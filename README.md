# 🧠 Intelligent Business Strategy Orchestrator

An AI-driven, MBA-style executive decision system that provides comprehensive business analysis, strategic recommendations, and executive reports.

## ✨ Features

- **AI-Powered Analysis**: Uses LangChain and Groq LLM for intelligent business insights
- **Multi-Agent System**: CEO, Finance, Marketing, HR, and Strategy agents working together
- **Financial Analysis**: Comprehensive profit/loss analysis with risk assessment
- **Strategic Planning**: Data-driven strategy recommendations
- **Marketing Insights**: Channel performance and ROI analysis
- **Executive Reports**: Professional PDF and PowerPoint presentations
- **Interactive Dashboard**: Beautiful Streamlit-based web interface
- **Visual Analytics**: Charts and graphs for better data visualization

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Groq API key (get one from [Groq](https://console.groq.com/) - **FREE**)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/intelligent-business-strategy-orchestrator.git
cd intelligent-business-strategy-orchestrator
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Get your Groq API key (REQUIRED):**
   - Go to https://console.groq.com/
   - Sign up for a free account
   - Create an API key in the dashboard
   - Copy the key

5. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   **Important:** Replace `your_groq_api_key_here` with your actual API key!

6. **Run the application:**
```bash
streamlit run dashboard/app.py
```

The app will open in your browser at `http://localhost:8501`

### ⚠️ Important Notes for Testers

- **API Key is REQUIRED** - The app won't work without a Groq API key
- **Free API Key** - Groq offers free tier, no credit card needed
- **Sample Data Included** - You can test with `data/company_data.json` and `data/profit_loss.csv`
- **See TESTING_GUIDE.md** - For detailed testing instructions

## 📁 Project Structure

```
.
├── agents/              # AI agents (CEO, Finance, Marketing, HR, Strategy)
├── dashboard/           # Streamlit web interface
├── data/               # Sample data files
├── datasets/           # Additional datasets
├── graph/              # Decision graph workflow
├── llms/               # LLM configuration and utilities
├── reports/            # Report generation (PDF, PPT)
├── utils/              # Utility functions (finance, marketing, strategy engines)
├── main.py             # CLI entry point
└── requirements.txt    # Python dependencies
```

## 🎯 Usage

### Web Interface

1. Start the Streamlit app: `streamlit run dashboard/app.py`
2. Upload your business data (CSV format)
3. Upload profit & loss data (CSV format)
4. View real-time analysis and insights
5. Generate executive PDF and PPT reports

### Command Line

Run the full pipeline:
```bash
python main.py
```

This will process `data/company_data.json` and generate `output.json` with all analysis results.

## 📊 Data Format

### Business Data CSV
Should contain columns: `field`, `value`

Example:
```csv
field,value
revenue,1000000
expenses,750000
growth_rate,15%
team_size,25
industry,E-commerce
```

### Profit & Loss CSV
Should contain columns: `Month`, `Revenue`, `Expenses`

Example:
```csv
Month,Revenue,Expenses
Jan,100000,80000
Feb,110000,85000
Mar,120000,90000
```

## 🔧 Configuration

### API Keys
Add your Groq API key to `.env`:
```
GROQ_API_KEY=your_api_key_here
```

### Customization
- Modify agent prompts in `agents/` directory
- Adjust analysis logic in `utils/` directory
- Customize report templates in `reports/` directory

## 📈 Features in Detail

### Financial Analysis
- Revenue vs Expenses trend analysis
- Profit margin calculations
- Risk level assessment
- Financial health metrics

### Strategy Analysis
- Growth strategy recommendations
- Focus area prioritization
- Risk-based strategic planning

### Marketing Analysis
- Channel contribution analysis
- ROI calculations
- Marketing spend optimization

### Executive Reports
- Professional PDF reports with charts
- PowerPoint presentations with visualizations
- Clean, executive-ready formatting

## 🛠️ Technologies Used

- **Streamlit**: Web interface
- **LangChain**: LLM orchestration
- **LangGraph**: Multi-agent workflow
- **Groq**: Fast LLM inference
- **Pandas**: Data processing
- **Matplotlib**: Chart generation
- **ReportLab**: PDF generation
- **python-pptx**: PowerPoint generation

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🙏 Acknowledgments

- Built with LangChain and LangGraph
- Powered by Groq LLM
- UI inspired by Power BI and executive dashboards

