# 📈 Covered Call Optimizer

## ⚠️ Disclaimer

This tool is provided **for educational and informational purposes only**.  
Nothing in this repository constitutes financial, legal, or investment advice.  
By using this code, you acknowledge that you do so **at your own discretion and risk**.  
**I am not liable for any financial losses, outcomes, or decisions made** based on this tool or its outputs.  
Always consult with a licensed financial advisor before making investment decisions.  
By using, cloning, or modifying this code, you **agree to these terms**.

---

## 🧠 What This Tool Does

`cc_optimizer.ipynb` analyzes covered call options across all tickers listed in `stocks.txt` and calculates key features to help you identify the most attractive contracts based on reward vs. risk.

Given Schwab option chain data, it computes the following for each contract:

Let:

- **S** = underlying price  
- **K** = strike price  
- **B** = bid price of the call option  
- **DTE** = days to expiration  

Then it computes:

- **Stock Return Cap**  
  `stockReturnCap = max(0, K / S - 1)`

- **Premium Return**  
    ```
    if K < S:
        premiumReturn = (B / S) - (S / K - 1)
    else:
        premiumReturn = B / S
        ```


- **Annualized Premium Return**  
`annualizedPremiumReturn = (1 + premiumReturn) ** (252 / DTE) - 1`

- **Cost for 100 Shares**  
`costForUnderlying = S * 100`

- **Breakeven Point**  
`breakevenPoint = S - B`

- **Downside Protection**  
`downsideProtection = B / S`

- **Dollar Return on Premium**  
`dollarReturn = premiumReturn * costForUnderlying`

---

You can **sort and filter results in real time** to identify the highest yielding covered call setups based on return, downside protection, or breakeven price.

---

## ⚙️ Setup Instructions

### ✅ What You’ll Need:

1. A **Schwab API developer account** — register at [Schwab Developer Portal](https://developer.schwabapi.com) - this may take a few days.
2. Create a new app in your Schwab account and **note your client ID and secret**
3. Set the **redirect URI** to: `https://127.0.0.1`
4. Save your credentials in a `.env` file:
  ```bash
  APP_KEY=your_app_key
  APP_SECRET=your_client_secret
  AUTHORIZATION_TOKEN=your_auth_token
  ```
5. For additional help setting up your Schwab app, check out [Tyler Bowers' Schwab API Guide](https://github.com/tylerebowers/Schwabdev)

---

### 🚀 Running the Optimizer

1. **Start the token handler**:
  ```
  python activate_tokens.py
  ```

2. A browser window will open — **log into your Schwab account** and follow instructions until you see a blank page

3. **Copy the URL** from the blank page back into the terminal when prompted

4. Keep `activate_tokens.py` running in the background (it auto-refreshes tokens every 30 minutes)

5. Now you're ready to run `cc_optimizer.py` and fetch real-time covered call data
