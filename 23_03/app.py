import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import os
from flask import Flask, render_template, request

app = Flask(__name__)

def get_data():
    try:
        if not os.path.exists('CO2.csv'):
            return pd.DataFrame({'Day': range(1, 11), 'CO2': [400, 450, 850, 900, 1100, 1050, 700, 600, 950, 1200]})
        df = pd.read_csv('CO2.csv')
        df.columns = df.columns.str.replace('"', '').str.strip()
        df['Day'] = pd.to_numeric(df['Day'], errors='coerce')
        df['CO2'] = pd.to_numeric(df['CO2'], errors='coerce')
        df = df.dropna(subset=['Day', 'CO2'])
        return df.sort_values('Day')
    except Exception:
        return pd.DataFrame(columns=['Day', 'CO2'])

@app.route('/', methods=['GET', 'POST'])
def index():
    df = get_data()
    all_days = df['Day'].unique().tolist()
    
    view_mode = request.form.get('view_mode')
    selected_day = request.form.get('day_select')
    
    plot_url = None
    selected_data = None
    status_info = None

    if view_mode == 'graph':
        fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
        limit_green, limit_yellow = 800, 1000
        
        if not selected_day or selected_day == "":
            # Kopskata līniju grafiks
            ax.plot(df['Day'], df['CO2'], color='#3498db', lw=2, label='CO2 līmenis')
            ax.fill_between(df['Day'], df['CO2'], color='#3498db', alpha=0.1)
            ax.set_title('Kopējā CO2 dinamika', fontsize=14, pad=15)
        else:
            day_int = int(selected_day)
            # Atlasām logu +/- 10 dienas ap izvēlēto dienu labākai redzamībai
            f_df = df[(df['Day'] >= day_int - 10) & (df['Day'] <= day_int + 10)].copy()
            
            colors = ['#2ecc71' if v <= limit_green else '#f1c40f' if v <= limit_yellow else '#e74c3c' for v in f_df['CO2']]
            
            # Zīmējam stabiņus
            bars = ax.bar(f_df['Day'], f_df['CO2'], color=colors, edgecolor='white', linewidth=0.5)
            
            # Atrodam un izceļam izvēlēto dienu
            for bar in bars:
                # bar.get_x() atgriež stabiņa kreiso malu, pieskaitām pusi platuma, lai dabūtu centru
                bar_center = round(bar.get_x() + bar.get_width()/2)
                if bar_center == day_int:
                    bar.set_edgecolor('black') # Melna apmale
                    bar.set_linewidth(2.5)     # Bieza apmale
                    height = bar.get_height()
                    # Pievienojam tekstu virs stabiņa
                    ax.text(bar.get_x() + bar.get_width()/2, height + 15, 
                            f'{int(height)}', ha='center', va='bottom', 
                            fontweight='bold', fontsize=12, color='black')

            ax.set_title(f'Detalizēts grafiks: {day_int}. diena', fontsize=14, pad=15)

        # Fonu krāsas zonām
        ax.axhspan(0, limit_green, color='green', alpha=0.05, label='Norma')
        ax.axhspan(limit_green, limit_yellow, color='orange', alpha=0.05, label='Vidēji')
        ax.axhspan(limit_yellow, ax.get_ylim()[1] + 100, color='red', alpha=0.05, label='Bīstami')
        
        ax.set_xlabel('Diena')
        ax.set_ylabel('CO2 (ppm)')
        ax.legend(loc='upper right', fontsize='small')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)

    elif view_mode == 'data' and selected_day:
        day_int = int(selected_day)
        row = df[df['Day'] == day_int]
        if not row.empty:
            selected_data = float(row.iloc[0]['CO2'])
            if selected_data <= 800: status_info = ("TEICAMI", "c-green")
            elif selected_data <= 1000: status_info = ("VIDĒJI", "c-yellow")
            else: status_info = ("BĪSTAMI", "c-red")

    return render_template('index.html', 
                           all_days=all_days, 
                           view_mode=view_mode, 
                           plot_url=plot_url, 
                           selected_day=selected_day,
                           selected_data=selected_data,
                           status_info=status_info)

if __name__ == '__main__':
    app.run(debug=True)