# BUDDY AI Assistant

A comprehensive AI assistant with personal productivity features, health guidance, and intelligent conversation capabilities.

## 🌟 Features

- **Personal Assistant**: Task management, notes, calendar, contacts, file management
- **Communication**: Email templates and communication tracking  
- **Research Management**: Knowledge base and learning goals
- **Health Guidance**: Health tips and medical information
- **Weather & Forecasts**: Current weather and predictions
- **Entertainment**: Jokes, quotes, and fun interactions
- **Voice Interface**: Speech recognition and synthesis (local)
- **Web Interface**: Clean, responsive web UI

## 🚀 Live Demo

Visit: [Your deployed URL will go here]

## 💻 Local Development

### Prerequisites
- Python 3.11 or higher
- Git

### Setup
```bash
git clone https://github.com/2021WB15454/BUDDY_AI.git
cd BUDDY_AI
pip install -r requirements.txt
python main.py
```

Visit `http://localhost:8000` to use the web interface.

### Configuration
1. Copy `.env.example` to `.env`
2. Add your API keys (optional for basic functionality)
3. Customize settings in `utils/config.py`

## 🌐 Deployment

### Render (Recommended)
1. Fork this repository
2. Connect to [Render](https://render.com)
3. Create a new Web Service
4. Connect your GitHub repository
5. Set environment variables for API keys
6. Deploy!

### Other Platforms
- **Railway**: Connect GitHub repo, set environment variables
- **Heroku**: Use `Procfile` and `runtime.txt` included
- **Vercel/Netlify**: For static frontend deployment

## 🔧 Environment Variables

For production deployment, set these environment variables:

```
PORT=8000
ENVIRONMENT=production
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
```

## 📁 Project Structure

```
BUDDY AI ASSISTANT/
├── core/                  # Core AI logic
├── skills/               # Individual skill modules
├── interfaces/           # Web and voice interfaces
├── utils/               # Utilities and configuration
├── learning_data/       # Data persistence
├── static/             # Web UI assets
└── tests/              # Integration tests
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

- Create an issue for bug reports
- Star the repository if you find it useful
- Follow for updates

## 🔮 Future Plans

- Mobile app development
- Advanced AI integrations
- Plugin system for custom skills
- Multi-language support
- Enterprise features

---

Made with ❤️ by [Your Name]
