import axios from 'axios';
import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load .env from the parent directory's .scr folder
dotenv.config({ 
  path: path.resolve(__dirname, '../../.scr/.env'),
  quiet: true 
});

const TB_URL = process.env.TB_URL || 'http://204.168.202.5:8080';
const USERNAME = process.env.TB_USERNAME;
const PASSWORD = process.env.TB_PASSWORD;

let jwtToken: string | null = null;
let tokenExpiration: number = 0;

async function login() {
  if (jwtToken && Date.now() < tokenExpiration) {
    return jwtToken;
  }

  try {
    const response = await axios.post(`${TB_URL}/api/auth/login`, {
      username: USERNAME,
      password: PASSWORD
    });
    jwtToken = response.data.token;
    // Basic JWT decode to get expiration if needed, or just assume 2 hours
    tokenExpiration = Date.now() + 2 * 60 * 60 * 1000; 
    return jwtToken;
  } catch (error: any) {
    console.error('Login failed:', error.response?.data || error.message);
    throw new Error('Could not authenticate with ThingsBoard');
  }
}

export async function getCustomers(pageSize = 100, page = 0) {
  const token = await login();
  const response = await axios.get(`${TB_URL}/api/customers`, {
    params: { pageSize, page },
    headers: { 'X-Authorization': `Bearer ${token}` }
  });
  return response.data;
}

export async function getDevices(pageSize = 100, page = 0, type = '') {
  const token = await login();
  const response = await axios.get(`${TB_URL}/api/tenant/devices`, {
    params: { pageSize, page, type },
    headers: { 'X-Authorization': `Bearer ${token}` }
  });
  return response.data;
}

export async function getUsers(pageSize = 100, page = 0) {
  const token = await login();
  const logPath = 'c:/01 - Sentivis/Sentivis SIM/mcp-thingsboard/mcp_debug.log';
  try {
    fs.appendFileSync(logPath, `Calling /api/users with pageSize=${pageSize}, page=${page}\n`);
    const response = await axios.get(`${TB_URL}/api/users`, {
      params: { pageSize, page },
      headers: { 'X-Authorization': `Bearer ${token}` }
    });
    return response.data;
  } catch (error: any) {
    const errorData = JSON.stringify({
      status: error.response?.status,
      data: error.response?.data,
      params: { pageSize, page }
    }, null, 2);
    fs.appendFileSync(logPath, `Error in getUsers: ${errorData}\n`);
    throw error;
  }
}

export async function getCustomerDevices(customerId: string, pageSize = 100, page = 0) {
  const token = await login();
  const response = await axios.get(`${TB_URL}/api/customer/${customerId}/devices`, {
    params: { pageSize, page },
    headers: { 'X-Authorization': `Bearer ${token}` }
  });
  return response.data;
}
