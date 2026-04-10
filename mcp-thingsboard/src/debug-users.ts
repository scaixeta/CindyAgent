import axios from 'axios';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: path.resolve(__dirname, '../../.scr/.env') });

const TB_URL = process.env.TB_URL || 'http://204.168.202.5:8080';
const USERNAME = process.env.TB_USERNAME;
const PASSWORD = process.env.TB_PASSWORD;

async function debug() {
  try {
    const loginResp = await axios.post(`${TB_URL}/api/auth/login`, {
      username: USERNAME,
      password: PASSWORD
    });
    const token = loginResp.data.token;
    
    console.log('Testing /api/users...');
    try {
      const resp = await axios.get(`${TB_URL}/api/users`, {
        params: { pageSize: 10, page: 0 },
        headers: { 'X-Authorization': `Bearer ${token}` }
      });
      console.log('Success /api/users:', JSON.stringify(resp.data, null, 2));
    } catch (e: any) {
      console.error('Error /api/users:', e.response?.status, e.response?.data);
    }

    console.log('Testing /api/tenant/users...');
    try {
      const resp2 = await axios.get(`${TB_URL}/api/tenant/users`, {
        params: { pageSize: 10, page: 0 },
        headers: { 'X-Authorization': `Bearer ${token}` }
      });
      console.log('Success /api/tenant/users:', JSON.stringify(resp2.data, null, 2));
    } catch (e: any) {
      console.error('Error /api/tenant/users:', e.response?.status, e.response?.data);
    }
  } catch (err: any) {
    console.error('Main error:', err.message);
  }
}

debug();
