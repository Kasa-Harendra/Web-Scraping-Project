import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class DataShow():
    def __init__(self, file_name):
        self.df = pd.read_csv(f'{file_name}.csv')
    def visualise_sale(self):
        df_sale_max = self.df.groupby('Company_name')['Sale Price (₹)'].max().to_dict()
        df_sale_min = self.df.groupby('Company_name')['Sale Price (₹)'].min().to_dict()
        plt.figure(figsize = (50,50))
        plt.plot(df_sale_max.keys(),df_sale_max.values(), color = 'r',label = 'Maximum Sale Price')
        plt.plot(df_sale_min.keys(),df_sale_min.values(),  color = 'g',linestyle = '--', alpha = 0.5, label = 'Minimum Sale Price')
        plt.grid(axis= 'y', color=  'b', linestyle= '-.', linewidth = 0.5, alpha = 0.5)
        plt.yticks(fontsize = 10)
        plt.xticks(fontsize = 5, rotation=90)
        plt.xlabel('Company name')
        plt.ylabel('Price in Rs')
        plt.legend()
        plt.show()

    def visualise_rating(self):
        plt.ylabel('Rating')
        plt.xlabel('Company name')
        df_rating = self.df.groupby('Company_name')['Rating'].mean().to_dict()
        plt.grid(axis = 'y', color = 'b', linestyle = '--', alpha = 0.5 )
        plt.bar(df_rating.keys(),df_rating.values(), color = 'g')
        plt.yticks(np.arange(0, 5.1, 0.5), fontsize = 10)
        plt.xticks(fontsize = 5, rotation=90)
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python app.py <output_file> <search_term> <count>")
        sys.exit(1)

    name = sys.argv[1] 
    search_term = sys.argv[2]
    count = sys.argv[3]

    os.system(f'cmd /c "scrapy crawl flipscraper -a search_term={search_term} -a num={count} -O {name}.csv"')

    path = f'flipkart\{name}.csv'

    os.system('cmd /c cls')




