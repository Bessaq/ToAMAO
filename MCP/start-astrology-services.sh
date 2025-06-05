#!/bin/bash
# Script para iniciar a API ToAMAO e o servidor MCP

echo "🚀 Iniciando API ToAMAO..."
cd /home/scrapybara/ToAMAO
python3 main.py &
API_PID=$!

echo "⏳ Aguardando API inicializar..."
sleep 5

echo "🌟 Iniciando Servidor MCP de Astrologia..."
cd /home/scrapybara
python3 mcp-astrology-server.py &
MCP_PID=$!

echo "✅ Serviços iniciados!"
echo "📊 API ToAMAO: PID $API_PID"
echo "🔧 MCP Server: PID $MCP_PID"
echo ""
echo "Para parar os serviços:"
echo "kill $API_PID $MCP_PID"

wait
