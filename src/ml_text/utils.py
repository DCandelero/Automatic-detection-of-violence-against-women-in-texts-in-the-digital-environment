import os
from matplotlib import pyplot as plt

from scikitplot.metrics import plot_roc_curve, plot_precision_recall_curve
from visualization import make_confusion_matrix

def save_results(results:dict, results_folder_path:str, summary_run:dict):
    os.makedirs(results_folder_path, exist_ok = True) 

    file_path = os.path.join(results_folder_path, 'summary_run.txt')
    with open(file_path, 'w') as file:
        file.write(str(summary_run))

    file_path = os.path.join(results_folder_path, 'confusion_matrix.png')
    make_confusion_matrix(results['cm'], 
                          categories=['contém agressão', 'não contém agressão'], 
                          figsize=(8,6), 
                          cbar=False, 
                          sum_stats=False, 
                          save_path=file_path)
    
    if 'predictions_probs' in results.keys():
        file_path = os.path.join(results_folder_path, 'ROC_curve.png')
        plot_roc_curve(results['true_labels'], results['predictions_probs'])
        plt.savefig(file_path) 
        file_path = os.path.join(results_folder_path, 'PR_curve.png')
        plot_precision_recall_curve(results['true_labels'], results['predictions_probs'])
        plt.savefig(file_path) 
        

    