/** @type {import('next').NextConfig} */
const CopyPlugin = require('copy-webpack-plugin');
const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');
const path = require('path');

const {createProxyMiddleware} = require('http-proxy-middleware');


const nextConfig = {
  // output: 'export',
  experimental: {
    esmExternals: 'loose',
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  env: {
    API_BASE_URL: process.env.API_BASE_URL,
  },
  trailingSlash: true,
  images: { unoptimized: true },

  async rewrites () {
    return [
      {
        source: '/db-gpt-server/:path*',
        destination: 'http://127.0.0.1:5670/:path*',
      },
    ]
  },
  async serverMiddleware () {
    const app = require('express')();
    app.use(
      '/db-gpt-server',
      createProxyMiddleware({
        target: 'http://127.0.0.1:5670',
        changeOrigin: true,
      })
    );
    return app;
  },


  webpack: (config, { isServer }) => {
    config.resolve.fallback = { fs: false };
    if (!isServer) {
      config.plugins.push(
        new CopyPlugin({
          patterns: [
            {
              from: path.join(__dirname, 'node_modules/@oceanbase-odc/monaco-plugin-ob/worker-dist/'),
              to: 'static/ob-workers'
            },
          ],
        })
      )
      // 添加 monaco-editor-webpack-plugin 插件
      config.plugins.push(
        new MonacoWebpackPlugin({
          // 你可以在这里配置插件的选项，例如：
          languages: ['sql'],
          filename: 'static/[name].worker.js'
        })
      );
    }
    return config;
  }
};

module.exports = nextConfig;
