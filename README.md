# AWTRIX Stock Display 📈

[![GitHub Release](https://img.shields.io/github/v/release/Raythekool/ha-awtrix-yahoofinance-stock?style=flat-square)](https://github.com/Raythekool/ha-awtrix-yahoofinance-stock/releases)
[![GitHub License](https://img.shields.io/github/license/Raythekool/ha-awtrix-yahoofinance-stock?style=flat-square)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Raythekool/ha-awtrix-yahoofinance-stock?style=flat-square)](https://github.com/Raythekool/ha-awtrix-yahoofinance-stock/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/Raythekool/ha-awtrix-yahoofinance-stock?style=flat-square)](https://github.com/Raythekool/ha-awtrix-yahoofinance-stock/issues)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Blueprint-41BDF5?style=flat-square&logo=home-assistant)](https://www.home-assistant.io/)
[![AWTRIX](https://img.shields.io/badge/AWTRIX-3-orange?style=flat-square)](https://blueforcer.github.io/awtrix3/)

Home Assistant Blueprint to display Yahoo Finance stock data on your AWTRIX 3 LED matrix device with dynamic colors and icons.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9qjudo87ha9ntscsjplz.gif)

## ⚠️ Requirements

Before using this blueprint, make sure you have:

1. **Home Assistant** with blueprint support (2024.6.0 or newer)
2. **AWTRIX 3** device configured and connected via MQTT
3. **Yahoo Finance Integration** installed and configured ([documentation](https://www.home-assistant.io/integrations/yahoofinance/))

## 📦 Installation

### Method 1: Automatic Import (Recommended)

1. Click the button below to import the blueprint:

   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FRaythekool%2Fha-awtrix-yahoofinance-stock%2Fblob%2Fmain%2Fawtrix_stock_display.yaml)

2. Click "Import Blueprint" in your Home Assistant
3. The blueprint will be available in your automations

### Method 2: Manual Import

1. Go to Home Assistant → Settings → Automations & Scenes → Blueprints
2. Click the "Import Blueprint" button
3. Enter this URL:

   ```text
   https://github.com/Raythekool/ha-awtrix-yahoofinance-stock/blob/main/awtrix_stock_display.yaml
   ```

4. Click "Preview" and then "Import Blueprint"

### Method 3: Local File

1. Download the `awtrix_stock_display.yaml` file
2. Copy the file to the `blueprints/automation/` folder in your Home Assistant configuration
3. Restart Home Assistant or reload automations

## 🎨 Setup Yahoo Finance Integration

Before using this blueprint, you need to set up the Yahoo Finance integration:

1. Go to Home Assistant → Settings → Devices & Services
2. Click "Add Integration" and search for "Yahoo Finance"
3. Enter the stock symbol you want to track (e.g., `AAPL`, `TSLA`, `BTC-USD`)
4. The integration will create a sensor entity (e.g., `sensor.yahoofinance_aapl`)

Repeat for each stock you want to display.

## 🚀 Usage

1. Go to Home Assistant → Settings → Automations & Scenes
2. Click "Create Automation" → "Use a blueprint"
3. Select "AWTRIX Stock Display 📈"
4. Configure the parameters:
   - **AWTRIX Device**: Select your AWTRIX device(s)
   - **Yahoo Finance Stock Sensor**: Select the stock sensor (e.g., `sensor.yahoofinance_aapl`)
   - **Stock Symbol/Name**: Enter display name (e.g., `AAPL`, `Tesla`)
   - **AWTRIX App Name**: Unique identifier (e.g., `stock_aapl`)
   - **Change Threshold**: Percentage for color changes (default: 0.2%)
   - **App Lifetime**: Auto-refresh interval in seconds (default: 900 = 15 min)
   - **Repeat Count**: Times to display (default: 1)
   - **Scroll Speed**: Text scroll speed (default: 100)
   - **Currency Symbol**: Currency to display (default: €)
5. Save the automation

### Multiple Stocks

To display multiple stocks, create separate automations for each stock with different app names:

- Stock 1: App Name = `stock_aapl`
- Stock 2: App Name = `stock_tsla`
- Stock 3: App Name = `stock_btc`

## 🎯 Features

- **Dynamic Colors**: Automatic color coding based on market performance
  - 🟢 Green: Price change > threshold (default +0.2%)
  - 🔴 Red: Price change < -threshold (default -0.2%)
  - ⚪ White: Change within threshold range

- **Dynamic Icons**: Market trend indicators
  - 📈 Up arrow (40160): Stock trending up
  - 📉 Down arrow (40176): Stock trending down
  - ➡️ Neutral (40161): Minimal change

- **Real-time Updates**: Triggers on:
  - Stock price changes from Yahoo Finance
  - Every 15 minutes (time pattern)

- **Customizable Display**:
  - Adjustable change threshold
  - Custom currency symbols
  - Configurable scroll speed
  - Auto-refresh lifetime

- **Multi-device Support**: Send to multiple AWTRIX devices simultaneously

- **Debug Logging**: Automatic system log entries for troubleshooting

## 📊 Display Format

The display shows:

```
AAPL 150.25€ (+2.5%)
```

- **AAPL**: Stock symbol/name
- **150.25€**: Current price with currency
- **(+2.5%)**: Percentage change (color-coded)
- **Icon**: Trend arrow (changes based on performance)

## 🔧 Advanced Configuration

### Change Threshold

The threshold determines when colors and icons change:

- **Low threshold (0.1%)**: More sensitive, changes color frequently
- **High threshold (1.0%)**: Less sensitive, only major changes trigger colors
- **Default (0.2%)**: Balanced for typical stock volatility

### App Lifetime

Controls how long the stock display remains on AWTRIX:

- **Short (300s = 5 min)**: Frequent updates, good for volatile stocks
- **Medium (900s = 15 min)**: Default, balanced update frequency
- **Long (3600s = 1 hour)**: Less frequent updates, reduces API calls

### Currency Symbols

Supports any currency symbol:

- `€` - Euro (default)
- `$` - Dollar
- `£` - Pound
- `¥` - Yen
- Or use empty string for no symbol

## 📝 Notes

- The blueprint uses "restart" mode to handle rapid price changes
- Stock data is published to MQTT topic `{prefix}/custom/{app_name}`
- Icons are from LaMetric library (40160, 40161, 40176)
- Updates trigger on state changes and every 15 minutes via time pattern
- System log entries are created for each update (info level)

## 🐛 Troubleshooting

### Stock Not Displaying

1. Check Yahoo Finance integration is working: Go to Developer Tools → States and verify your sensor shows data
2. Verify AWTRIX device is online and connected to MQTT
3. Check Home Assistant logs (Settings → System → Logs) for error messages
4. Ensure app name is unique if running multiple stocks

### Colors Not Changing

1. Verify the stock has actual price changes
2. Check if change threshold is too high
3. Review the `regularMarketChangePercent` attribute in Developer Tools → States

### Display Text Too Long

1. Use shorter stock symbols/names
2. Adjust scroll speed to make text scroll faster
3. Remove currency symbol if needed

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or pull request.

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more details.

## 🙏 Credits

- Yahoo Finance Integration: [Home Assistant](https://www.home-assistant.io/integrations/yahoofinance/)
- AWTRIX 3: [Blueforcer](https://github.com/Blueforcer/awtrix3)
- Icons: [LaMetric](https://developer.lametric.com/icons)

## ⭐ Show Your Support

If you find this blueprint useful, please consider:

- ⭐ Starring this repository
- 🐛 Reporting issues
- 💡 Suggesting new features
- 🔀 Contributing improvements
