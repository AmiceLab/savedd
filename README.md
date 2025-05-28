# SaveDD — A Community-Powered Receipt Analyzer and Price Comparison Tool

**SaveDD** is a Django-based web application that enables users to digitize physical receipts by scanning them through their phone’s camera or uploading image files. Built to empower communities through collaborative data, SaveDD extracts receipt details, stores them in a secure backend, and allows users to compare prices across stores — all while preserving privacy.

---

## 🔍 Key Features

- **📸 Receipt Upload via Mobile & Web**
  - Users can take a photo or upload an image of a receipt.
  - JavaScript-based frontend resizes and enhances image clarity for optimal OCR performance.

- **🧠 OCR Text Extraction**
  - Re-coloring and contrast adjustment performed in-browser before submission.
  - Tesseract.js integrated to extract item names and prices from images.
  - Outputs structured JSON for further processing.

- **💾 Django Backend & Data Storage**
  - Secure, scalable storage of receipt data and user-submitted metadata.
  - Admin interface for reviewing and approving new entries.

- **📊 Community Price Comparison**
  - Aggregates receipt data to show price fluctuations and store comparisons.
  - Users can contribute anonymously or with optional accounts.

---

## 💻 Tech Stack

- **Frontend:** HTML, CSS, JavaScript (Image resizing, color adjustment, file handling)
- **Backend:** Python, Django, Django REST Framework
- **OCR Engine:** Tesseract.js
- **DevOps & Deployment:** Git, GitHub Actions (CI/CD), Nginx, Gunicorn
- **Database:** PostgreSQL
- **Cloud:** DigitalOcean (planned)
- **Security:** .env management, Django middleware for CSRF/authentication

---

## ⚙️ Features Under Development

- **🔗 API Access for Developers**
  - OpenAPI / Swagger integration for programmatic access to receipt datasets.
  - Filter by location, store, category, or date.

- **🧠 Agentic AI Integration**
  - Use of LangChain + LLMs to generate actionable insights from receipt patterns.
  - Personalized nutrition or financial suggestions based on spending history.

- **📈 Data Visualization Dashboard**
  - Interactive charts for users to view savings, store comparisons, and common items.
  - Built with D3.js / Chart.js (planned).

- **🤝 Community Collaboration**
  - Users can label receipts or correct OCR results (crowdsourced improvement).
  - Rewards system (gamified) to encourage participation.

---

## 🚀 Why SaveDD?

- Designed as a **real-world solution** to reduce information asymmetry in consumer goods pricing.
- Encourages **digital literacy** and **community cooperation** while collecting useful open data.
- Supports **price transparency** and has potential applications in **policy advocacy**, **nutrition analytics**, and **anti-inflation monitoring**.

---

## 🧑‍💻 Built By

SaveDD is developed and maintained by a software engineer with 7+ years of experience in full-stack development, AI, and HealthTech. The project reflects a strong cross-domain skillset in:

- Cloud Architecture & Deployment
- OCR and Image Processing
- Full-Stack Web Development (Django / JS)
- API Design and Documentation (OpenAPI)
- Machine Learning and Agentic AI Integration
- Agile Team Leadership and UX Collaboration

---

## 📬 Future Plans

- Add user registration and personalized dashboards
- Launch browser extensions for instant receipt scanning
- Partner with local communities for broader data collection
- Submit for open data grants and innovation awards

---

## 📄 License

MIT License — Open-source contribution welcome!

---

## 🤝 Contributing

Pull requests, issue reports, and feedback are warmly welcome. Let’s build a fairer pricing ecosystem together 💡

