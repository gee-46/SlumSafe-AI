# 🚀 SlumSafe AI: Deployment Guide

Deploying SlumSafe AI is straightforward because it is built on the Streamlit framework. Below is the recommended path for a zero-cost, high-performance deployment.

---

## 1. Primary Option: Streamlit Community Cloud (Recommended)
This is the fastest and easiest way to get your app live on a public URL.

### **Step-by-Step Deployment:**
1.  **Sync to GitHub:** Ensure all your latest changes (including `requirements.txt`) are pushed to your GitHub repository (`gee-46/SlumSafe-AI`).
2.  **Sign In:** Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in using your GitHub account.
3.  **New App:** Click the **"New app"** button.
4.  **Configure:**
    *   **Repository:** Select `gee-46/SlumSafe-AI`.
    *   **Branch:** Select `main`.
    *   **Main file path:** Type `app.py`.
5.  **Deploy:** Click **"Deploy!"**. Your app will be live at a URL like `https://slumsafe-ai.streamlit.app` in under 2 minutes.

---

## 2. Critical Note: Data Persistence
Since your app currently saves reports to a local `reports.csv`, you need to be aware of how cloud platforms handle files:

> [!WARNING]
> **Ephemeral Storage:** Most deployment platforms (Streamlit Cloud, Heroku, Render) reset their "disk" every time the app restarts or you push an update. This means your `reports.csv` might be wiped clean occasionally.

### **How to Fix This for Production:**
To ensure reports are permanent even after restarts, you have three simple options:
1.  **Streamlit Connections:** Use the built-in [Streamlit Google Sheets connection](https://docs.streamlit.io/knowledge-base/tutorials/databases/google-sheets) to save reports to a private Google Sheet.
2.  **Supabase / PostgreSQL:** A more professional "SQL" approach. Free tiers are available.
3.  **Amazon S3:** Store the CSV in a cloud bucket where it never gets deleted.

---

## 3. Alternative Hosting Platforms
If you need more control or want to host it on your own server:

*   **Render / Railway:** Both support Streamlit natively via `Docker` or `Python` runtimes. Great if you want to scale horizontally.
*   **AWS EC2 / DigitalOcean:** You can rent a VPS (Virtual Private Server), install Python, and run the app manually. This gives you 100% control over the disk, so your CSV files stay safe.

---

## 4. Final Checklist Before Launch
*   [x] **requirements.txt:** Ensure `streamlit-js-eval` and `scikit-learn` are listed.
*   [x] **Model File:** Ensure `model/model.pkl` is pushed to GitHub.
*   [x] **Favicon & Title:** Already professionally configured.

**All latest codes are pushed to GitHub. You are ready to launch!**
