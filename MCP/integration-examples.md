# Exemplos de Integração - Servidor MCP de Astrologia

Este documento mostra como integrar o servidor MCP de Astrologia em diferentes aplicações e clientes.

## 1. Integração com Claude Desktop

### Configuração
Adicione ao arquivo de configuração do Claude Desktop:

```json
{
  "mcpServers": {
    "astrology": {
      "command": "python3",
      "args": ["/caminho/para/mcp-astrology-server.py"],
      "env": {
        "API_BASE_URL": "http://localhost:8000",
        "API_KEY": "testapikey"
      }
    }
  }
}
```

### Exemplo de Conversa
```
Usuário: "Pode calcular meu mapa natal? Nasci em 15/03/1990 às 14:30 em São Paulo"

Claude: Vou calcular seu mapa natal usando os dados fornecidos.

[Usa calculate_natal_chart com os parâmetros]

Resultado: Seu Sol está em Peixes na Casa 7, Lua em Virgem na Casa 2...
```

## 2. Integração com API Personalizada

### Cliente Python
```python
import asyncio
import json
from mcp.client import create_client

async def get_natal_chart(birth_data):
    async with create_client() as client:
        result = await client.call_tool(
            "calculate_natal_chart",
            birth_data
        )
        return result

# Uso
birth_data = {
    "name": "João",
    "year": 1990,
    "month": 3,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "latitude": -23.5505,
    "longitude": -46.6333,
    "tz_str": "America/Sao_Paulo"
}

chart = asyncio.run(get_natal_chart(birth_data))
```

### Cliente JavaScript/TypeScript
```typescript
import { McpClient } from '@modelcontextprotocol/sdk/client/index.js';

class AstrologyClient {
  private client: McpClient;

  async calculateNatalChart(birthData: any) {
    const result = await this.client.callTool(
      'calculate_natal_chart',
      birthData
    );
    return result;
  }

  async getCurrentTransits(date: Date, location: any) {
    const transitData = {
      year: date.getFullYear(),
      month: date.getMonth() + 1,
      day: date.getDate(),
      hour: date.getHours(),
      minute: date.getMinutes(),
      ...location
    };

    return await this.client.callTool(
      'get_current_transits',
      transitData
    );
  }
}
```

## 3. Integração Web

### Frontend React
```jsx
import React, { useState } from 'react';

const AstrologyApp = () => {
  const [chart, setChart] = useState(null);
  const [loading, setLoading] = useState(false);

  const calculateChart = async (birthData) => {
    setLoading(true);
    try {
      const response = await fetch('/api/astrology/natal-chart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(birthData)
      });
      const result = await response.json();
      setChart(result);
    } catch (error) {
      console.error('Erro ao calcular mapa:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Calculadora Astrológica</h1>
      {/* Formulário de entrada */}
      {chart && (
        <div>
          <h2>Seu Mapa Natal</h2>
          {/* Exibir resultados */}
        </div>
      )}
    </div>
  );
};
```

### Backend Express.js
```javascript
const express = require('express');
const { McpClient } = require('@modelcontextprotocol/sdk/client');

const app = express();
const astrologyClient = new McpClient();

app.post('/api/astrology/natal-chart', async (req, res) => {
  try {
    const result = await astrologyClient.callTool(
      'calculate_natal_chart',
      req.body
    );
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => {
  console.log('Servidor rodando na porta 3000');
});
```

## 4. Chatbot WhatsApp/Telegram

### Bot com Node.js
```javascript
const { Client } = require('whatsapp-web.js');
const { McpClient } = require('@modelcontextprotocol/sdk/client');

const whatsapp = new Client();
const astrology = new McpClient();

whatsapp.on('message', async (message) => {
  if (message.body.startsWith('/mapa')) {
    // Parselar dados de nascimento da mensagem
    const birthData = parseBirthData(message.body);
    
    try {
      const chart = await astrology.callTool(
        'calculate_natal_chart',
        birthData
      );
      
      await message.reply(formatChartForWhatsApp(chart));
    } catch (error) {
      await message.reply('Erro ao calcular mapa natal.');
    }
  }
});

function parseBirthData(messageText) {
  // Lógica para extrair dados de nascimento
  // Exemplo: "/mapa 15/03/1990 14:30 São Paulo"
}

function formatChartForWhatsApp(chart) {
  // Formatar dados do mapa para WhatsApp
  return `🌟 Seu Mapa Natal:
Sol: ${chart.planets.sun.sign}
Lua: ${chart.planets.moon.sign}
Ascendente: ${chart.ascendant.sign}`;
}
```

## 5. Aplicação Mobile Flutter

### Dart/Flutter
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class AstrologyService {
  static const String baseUrl = 'http://localhost:3000/api/astrology';

  static Future<Map<String, dynamic>> calculateNatalChart(
    Map<String, dynamic> birthData
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/natal-chart'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(birthData),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Erro ao calcular mapa natal');
    }
  }
}

// Widget Flutter
class NatalChartWidget extends StatefulWidget {
  @override
  _NatalChartWidgetState createState() => _NatalChartWidgetState();
}

class _NatalChartWidgetState extends State<NatalChartWidget> {
  Map<String, dynamic>? chart;

  void _calculateChart() async {
    final birthData = {
      'name': 'João',
      'year': 1990,
      'month': 3,
      'day': 15,
      'hour': 14,
      'minute': 30,
      'latitude': -23.5505,
      'longitude': -46.6333,
      'tz_str': 'America/Sao_Paulo'
    };

    try {
      final result = await AstrologyService.calculateNatalChart(birthData);
      setState(() {
        chart = result;
      });
    } catch (e) {
      // Tratar erro
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Mapa Natal')),
      body: chart != null
          ? ChartDisplay(chart: chart!)
          : Center(child: CircularProgressIndicator()),
      floatingActionButton: FloatingActionButton(
        onPressed: _calculateChart,
        child: Icon(Icons.calculate),
      ),
    );
  }
}
```

## 6. Integração com WordPress

### Plugin PHP
```php
<?php
/**
 * Plugin Name: Astrologia MCP
 * Description: Integração com servidor MCP de astrologia
 */

class AstrologyMCP {
    private $api_url = 'http://localhost:3000/api/astrology';
    
    public function calculate_natal_chart($birth_data) {
        $response = wp_remote_post($this->api_url . '/natal-chart', [
            'headers' => ['Content-Type' => 'application/json'],
            'body' => json_encode($birth_data)
        ]);
        
        if (is_wp_error($response)) {
            return false;
        }
        
        return json_decode(wp_remote_retrieve_body($response), true);
    }
}

// Shortcode para exibir mapa natal
function astrology_shortcode($atts) {
    $astrology = new AstrologyMCP();
    
    // Lógica para obter dados e exibir mapa
    return '<div class="astrology-chart">Mapa Natal...</div>';
}
add_shortcode('mapa_natal', 'astrology_shortcode');
?>
```

## 7. Ferramentas de Linha de Comando

### CLI Python
```python
#!/usr/bin/env python3
import argparse
import asyncio
from mcp.client import create_client

async def main():
    parser = argparse.ArgumentParser(description='CLI Astrologia')
    parser.add_argument('--natal', action='store_true', help='Calcular mapa natal')
    parser.add_argument('--name', type=str, help='Nome')
    parser.add_argument('--date', type=str, help='Data nascimento (DD/MM/AAAA)')
    parser.add_argument('--time', type=str, help='Hora (HH:MM)')
    parser.add_argument('--location', type=str, help='Localização')
    
    args = parser.parse_args()
    
    if args.natal:
        birth_data = parse_birth_data(args)
        
        async with create_client() as client:
            result = await client.call_tool('calculate_natal_chart', birth_data)
            print_chart_result(result)

def parse_birth_data(args):
    # Converter argumentos em dados estruturados
    pass

def print_chart_result(result):
    # Formatar e exibir resultado
    pass

if __name__ == '__main__':
    asyncio.run(main())
```

### Script Bash
```bash
#!/bin/bash
# astrology-cli.sh

function calculate_natal_chart() {
    local name="$1"
    local date="$2"
    local time="$3"
    local location="$4"
    
    curl -X POST http://localhost:3000/api/astrology/natal-chart \
         -H "Content-Type: application/json" \
         -d "{
            \"name\": \"$name\",
            \"date\": \"$date\",
            \"time\": \"$time\",
            \"location\": \"$location\"
         }" | jq .
}

# Uso: ./astrology-cli.sh "João" "15/03/1990" "14:30" "São Paulo"
calculate_natal_chart "$1" "$2" "$3" "$4"
```

## 8. Monitoramento e Analytics

### Dashboard em Python
```python
import streamlit as st
import pandas as pd
from datetime import datetime

st.title('Dashboard Astrológico')

# Interface para cálculo de mapas
with st.form('natal_chart_form'):
    name = st.text_input('Nome')
    birth_date = st.date_input('Data de Nascimento')
    birth_time = st.time_input('Hora de Nascimento')
    
    if st.form_submit_button('Calcular Mapa'):
        # Chamar servidor MCP
        chart_data = call_astrology_api({
            'name': name,
            'date': birth_date,
            'time': birth_time
        })
        
        # Exibir resultados
        st.json(chart_data)

# Gráficos e estatísticas
st.header('Estatísticas')
chart_stats = get_chart_statistics()
st.bar_chart(chart_stats)
```

## Conclusão

O servidor MCP de Astrologia oferece flexibilidade máxima para integração em:

- **Assistentes de IA** (Claude, ChatGPT, etc.)
- **Aplicações Web** (React, Vue, Angular)
- **Aplicações Mobile** (Flutter, React Native)
- **Chatbots** (WhatsApp, Telegram, Discord)
- **CMSs** (WordPress, Drupal)
- **Ferramentas CLI**
- **Dashboards** (Streamlit, Dash)

A arquitetura MCP permite que qualquer aplicação acesse funcionalidades astrológicas avançadas de forma padronizada e escalável.