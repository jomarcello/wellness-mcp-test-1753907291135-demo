module.exports = {
  apps: [
    // SpineAlign Center Server (Port 3000)
    {
      name: 'spinealign-server',
      script: 'npm',
      args: 'run dev',
      env: {
        PORT: 3000,
        PRACTICE_ID: 'spinealign',
        NODE_ENV: 'development'
      },
      watch: false,
      max_memory_restart: '100M',
      error_file: './logs/spinealign-err.log',
      out_file: './logs/spinealign-out.log',
      log_file: './logs/spinealign-combined.log'
    },
    // Smith Chiropractic Server (Port 3001) 
    {
      name: 'smith-server',
      script: 'npm',
      args: 'run dev',
      env: {
        PORT: 3001,
        PRACTICE_ID: 'smith',
        NODE_ENV: 'development'
      },
      watch: false,
      max_memory_restart: '100M',
      error_file: './logs/smith-err.log',
      out_file: './logs/smith-out.log',
      log_file: './logs/smith-combined.log'
    },
    // BeautyMed Thai Clinic Server (Port 3002)
    {
      name: 'beautymed-server',
      script: 'npm',
      args: 'run dev',
      env: {
        PORT: 3002,
        PRACTICE_ID: 'beautymed',
        NODE_ENV: 'development'
      },
      watch: false,
      max_memory_restart: '100M',
      error_file: './logs/beautymed-err.log',
      out_file: './logs/beautymed-out.log',
      log_file: './logs/beautymed-combined.log'
    },
    // SpineAlign Center Tunnel
    {
      name: 'spinealign-tunnel',
      script: 'npx',
      args: 'localtunnel --port 3000 --subdomain spinealign-center',
      env: {
        NODE_ENV: 'development'
      },
      restart_delay: 3000,
      max_restarts: 10,
      error_file: './logs/spinealign-tunnel-err.log',
      out_file: './logs/spinealign-tunnel-out.log',
      log_file: './logs/spinealign-tunnel-combined.log'
    },
    // Smith Chiropractic Tunnel
    {
      name: 'smith-tunnel',
      script: 'npx',
      args: 'localtunnel --port 3001 --subdomain smith-chiropractic',
      env: {
        NODE_ENV: 'development'
      },
      restart_delay: 3000,
      max_restarts: 10,
      error_file: './logs/smith-tunnel-err.log',
      out_file: './logs/smith-tunnel-out.log',
      log_file: './logs/smith-tunnel-combined.log'
    },
    // BeautyMed Thai Clinic Tunnel
    {
      name: 'beautymed-tunnel',
      script: 'npx',
      args: 'localtunnel --port 3002 --subdomain beautymed-thai',
      env: {
        NODE_ENV: 'development'
      },
      restart_delay: 3000,
      max_restarts: 10,
      error_file: './logs/beautymed-tunnel-err.log',
      out_file: './logs/beautymed-tunnel-out.log',
      log_file: './logs/beautymed-tunnel-combined.log'
    },
    // MCP Servers
    {
      name: 'playwright-mcp',
      script: 'node',
      args: 'dist/index.js',
      cwd: './nari-dia-env',
      interpreter: 'none',
      env: {
        NODE_ENV: 'production'
      },
      watch: false,
      instances: 1,
      exec_mode: 'cluster'
    },
    {
      name: 'notion-mcp',
      script: 'npx',
      args: '-y @notionhq/notion-mcp-server',
      env: {
        NODE_ENV: 'production',
        OPENAPI_MCP_HEADERS: '{"Authorization": "Bearer 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", "Notion-Version": "2022-06-28"}'
      },
      watch: false,
      instances: 1,
      exec_mode: 'cluster'
    },
    {
      name: 'browser-mcp',
      script: 'npx',
      args: '@modelcontextprotocol/server-browser-automation',
      env: {
        NODE_ENV: 'production'
      },
      watch: false,
      instances: 1,
      exec_mode: 'cluster'
    }
  ]
}; 