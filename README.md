# 🎯 Soonish (SH) Self Hosted

✨ A delightfully minimal countdown app that helps you track life's exciting moments! Built with FastAPI and sprinkled with modern web magic ✨

## 🌟 Features
- 📅 Create and manage event countdowns
- 🖼️ Beautiful images from Unsplash
- 🌓 Light/dark theme
- ⚡ Real-time updates with HTMX
- 🐳 Easy Docker deployment

## 🚀 Quick Start

### 1. 📸 Get Your Unsplash Powers
1. Visit [Unsplash Developers](https://unsplash.com/developers) 
2. Create your free developer account
3. Hit that "New Application" button
4. Grab your Access Key and Secret Key

### 2. ⚙️ Configuration
1. Clone this fabulous repo:
   ```bash
   git clone https://github.com/pypeaday/soonish-sh.git
   cd soonish-sh
2. Create a `.env` file:

   `cp .env.example .env`
3. Pop your unsplash credentials in there
4. 🐋 Launch with Docker
   `docker compose up --build -d`

That's it! Visit http://localhost:8000 and start counting down to your awesome events! 🎉

📝 Notes
Data is stored in a local SQLite database
Images are fetched from Unsplash in real-time
The app runs on port 8000 by default
🤝 Contributing
Found a bug? Want to add something cool? PRs are welcome!

📜 License
MIT - Go wild! 🎨

Made with 💖 and 🤖