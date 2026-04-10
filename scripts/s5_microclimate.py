#!/usr/bin/env python3
"""
S5 Microclimate Analytics — Sentivis IAOps

Lê o collection_log.txt da S4, extrai os 12 registros reais,
calcula tendências e marcadores operativos, e gera relatórios
em Markdown e JSON.

Uso:
    python scripts/s5_microclimate.py [--log PATH]
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def parse_collection_log(log_path: str) -> list[dict]:
    """Extrai registros do collection_log.txt."""
    records = []
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Pula cabeçalho, parser das linhas de dados
    # Estrutura: | # | Timestamp UTC | Temp (C) | Humidity (%) | Persisted |
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        if "Timestamp UTC" in line:
            continue
        if "---" in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 5:
            continue
        try:
            num = parts[1].strip()
            if not num.isdigit():
                continue
            timestamp = parts[2].strip()
            temp = float(parts[3].strip())
            humidity = float(parts[4].strip())
            records.append({
                "iter": int(num),
                "timestamp": timestamp,
                "temperature_c": temp,
                "humidity_pct": humidity,
            })
        except (ValueError, IndexError):
            continue

    return records


def classify_trend(values: list[float]) -> str:
    """Classifica tendência curta a partir de uma série de valores."""
    if len(values) < 2:
        return "insuficiente"
    diff = values[-1] - values[0]
    if abs(diff) < 0.5:
        return "estável"
    elif diff > 0:
        return "subindo"
    else:
        return "descendo"


def classify_temp_interval(temp_c: float) -> str:
    """Classifica temperatura contra referência operativa 18-24°C.
    
    NOTA: Esta é uma referência operativa, não uma verdade agronómica validada.
    """
    ref_low, ref_high = 18.0, 24.0
    if ref_low <= temp_c <= ref_high:
        return "dentro do intervalo de referência"
    elif temp_c < ref_low:
        return "abaixo do intervalo de referência"
    else:
        return "acima do intervalo de referência"


def humidity_persistent_count(records: list[dict], threshold: float = 85.0) -> tuple[int, int]:
    """Conta pontos acima do limiar de umidade (proxy de molhamento).
    
    Retorna (count, total).
    NOTA: Alta umidade não é equivalente a chuva — é proxy de molhamento foliar.
    """
    above = sum(1 for r in records if r["humidity_pct"] > threshold)
    return above, len(records)


def build_report(records: list[dict], log_path: str) -> dict:
    """Constrói o relatório estruturado."""
    if not records:
        return {"error": "nenhum registro encontrado"}

    temps = [r["temperature_c"] for r in records]
    humids = [r["humidity_pct"] for r in records]
    last = records[-1]

    temp_trend = classify_trend(temps)
    humid_trend = classify_trend(humids)
    temp_interval = classify_temp_interval(last["temperature_c"])
    humid_above, total = humidity_persistent_count(records)
    pct_above = round(humid_above / total * 100) if total > 0 else 0

    # Tendência da umidade分段
    if len(humids) >= 3:
        early_avg = sum(humids[:3]) / 3
        late_avg = sum(humids[-3:]) / 3
        humid_phase = "subida" if late_avg > early_avg + 1 else ("descendo" if late_avg < early_avg - 1 else "estável")
    else:
        humid_phase = classify_trend(humids)

    report = {
        "sprint": "S5",
        "source_log": str(log_path),
        "device": "NIMBUS-AERO (Cirrus)",
        "window": {
            "start": records[0]["timestamp"],
            "end": records[-1]["timestamp"],
            "points": len(records),
        },
        "current": {
            "temperature_c": last["temperature_c"],
            "humidity_pct": last["humidity_pct"],
        },
        "trends": {
            "temperature": temp_trend,
            "humidity": humid_phase,
        },
        "operative_markers": {
            "temp_interval": temp_interval,
            "humidity_above_85_count": humid_above,
            "humidity_above_85_pct": pct_above,
        },
        "summary": {
            "temperature": f"{last['temperature_c']}°C ({temp_trend})",
            "humidity": f"{last['humidity_pct']}% ({humid_phase})",
            "proxy_molhamento": f"{humid_above}/{total} pontos acima de 85%",
        },
        "safe_note": "Métricas são dados de campo. Intervalo 18-24°C é referência operativa, não validação agronómica.",
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    return report


def to_markdown(report: dict) -> str:
    """Converte relatório para Markdown."""
    if "error" in report:
        return f"# S5 Relatório de Microclima\n\n**Erro:** {report['error']}\n"

    lines = [
        "# S5 Relatório de Microclima — NIMBUS-AERO",
        "",
        f"**Data:** {datetime.utcnow().strftime('%Y-%m-%d')} | **Janela:** {report['window']['start']} - {report['window']['end']} UTC ({report['window']['points']} pontos)",
        "",
        "## Métricas Atuais",
        "",
        f"- **Temperatura:** {report['current']['temperature_c']}°C ({report['trends']['temperature']})",
        f"- **Umidade:** {report['current']['humidity_pct']}% ({report['trends']['humidity']})",
        "",
        "## Tendência",
        "",
        f"- **Umidade:** {report['trends']['humidity']}",
        f"- **Temperatura:** {report['trends']['temperature']}",
        "",
        "## Marcadores Operativos",
        "",
        f"- **Intervalo térmico:** {report['operative_markers']['temp_interval']} (referência 18-24°C — *referência operativa, não validação agronómica*)",
        f"- **Proxy de molhamento:** {report['summary']['proxy_molhamento']} (*alta umidade não é equivalente a chuva*)",
        "",
        "## Nota de Segurança",
        "",
        "*Métricas são dados de campo. Intervalo 18-24°C é referência operativa, não validação agronómica. 'Proxy de molhamento' indica umidade elevada, não chuva confirmada.*",
        "",
        f"*Gerado em: {report['generated_at']}*",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="S5 Microclimate Analytics")
    parser.add_argument("--log", default="artifacts/s4-cirrus/2026-04-10/collection_log.txt")
    args = parser.parse_args()

    log_path = Path(args.log)
    if not log_path.exists():
        print(f"Erro: arquivo não encontrado: {log_path}", file=sys.stderr)
        sys.exit(1)

    records = parse_collection_log(str(log_path))
    print(f"Registos extraídos: {len(records)}", file=sys.stderr)

    if not records:
        print("Erro: nenhum registo válido encontrado no log.", file=sys.stderr)
        sys.exit(1)

    report = build_report(records, str(log_path))

    # JSON
    json_out = Path("artifacts/s5-relatorio.json")
    json_out.parent.mkdir(parents=True, exist_ok=True)
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"JSON: {json_out}", file=sys.stderr)

    # Markdown
    md_out = Path("artifacts/s5-relatorio.md")
    with open(md_out, "w", encoding="utf-8") as f:
        f.write(to_markdown(report))
    print(f"Markdown: {md_out}", file=sys.stderr)

    # Stdout — resumo curto
    print("\n=== RESULTADO ===")
    print(f"Temperatura: {report['summary']['temperature']}")
    print(f"Umidade: {report['summary']['humidity']}")
    print(f"Proxy molhamento: {report['summary']['proxy_molhamento']}")


if __name__ == "__main__":
    main()
