import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import * as tbApi from './tb-api.js';

const server = new Server(
  {
    name: 'thingsboard-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

/**
 * Handle listing available tools.
 * Exposes tools for customers, devices, and users.
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'list_customers',
        description: 'Get a list of customers from ThingsBoard',
        inputSchema: {
          type: 'object',
          properties: {
            pageSize: { type: 'number', description: 'Maximum number of items' },
            page: { type: 'number', description: 'Page number' },
          },
        },
      },
      {
        name: 'list_devices',
        description: 'Get a list of all devices for the current tenant',
        inputSchema: {
          type: 'object',
          properties: {
            pageSize: { type: 'number' },
            page: { type: 'number' },
            type: { type: 'string', description: 'Device type filter' },
          },
        },
      },
      {
        name: 'list_customer_devices',
        description: 'Get a list of devices belonging to a specific customer',
        inputSchema: {
          type: 'object',
          properties: {
            customerId: { type: 'string', description: 'UUID of the customer' },
            pageSize: { type: 'number' },
            page: { type: 'number' },
          },
          required: ['customerId'],
        },
      },
      {
        name: 'list_users',
        description: 'Get a list of users (Responsible)',
        inputSchema: {
          type: 'object',
          properties: {
            pageSize: { type: 'number' },
            page: { type: 'number' },
          },
        },
      },
    ],
  };
});

/**
 * Handle tool calls.
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'list_customers': {
        const { pageSize, page } = (args as any) || {};
        const data = await tbApi.getCustomers(pageSize, page);
        return { content: [{ type: 'text', text: JSON.stringify(data, null, 2) }] };
      }
      case 'list_devices': {
        const { pageSize, page, type } = (args as any) || {};
        const data = await tbApi.getDevices(pageSize, page, type);
        return { content: [{ type: 'text', text: JSON.stringify(data, null, 2) }] };
      }
      case 'list_customer_devices': {
        const { customerId, pageSize, page } = (args as any) || {};
        const data = await tbApi.getCustomerDevices(customerId, pageSize, page);
        return { content: [{ type: 'text', text: JSON.stringify(data, null, 2) }] };
      }
      case 'list_users': {
        const { pageSize, page } = (args as any) || {};
        console.error('Calling list_users with:', { pageSize, page });
        const data = await tbApi.getUsers(pageSize, page);
        return { content: [{ type: 'text', text: JSON.stringify(data, null, 2) }] };
      }
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [{ type: 'text', text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});

/**
 * Start the server using stdio transport.
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('ThingsBoard MCP server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error in main():', error);
  process.exit(1);
});
