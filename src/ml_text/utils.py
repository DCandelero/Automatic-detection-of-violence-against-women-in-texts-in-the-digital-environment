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
                          categories=['não contém agressão', 'contém agressão'], 
                          figsize=(8,6), 
                          cbar=False, 
                          sum_stats=False, 
                          save_path=file_path)
    
    if 'predictions_probs' in results.keys():
        file_path = os.path.join(results_folder_path, 'ROC_curve.png')
        plot_roc_curve(y_true=results['true_labels'], 
                        y_probas=results['predictions_probs'],
                        title='Curvas ROC')
        plt.xlabel('Taxa de falsos positivos')
        plt.ylabel('Taxa de verdadeiros positivos')
        L=plt.legend()
        L.get_texts()[0].set_text('Curva ROC - "Não contém agressão" (Á'+ L.get_texts()[0].get_text()[-11:])
        L.get_texts()[1].set_text('Curva ROC - "Contém agressão" (Á'+ L.get_texts()[1].get_text()[-11:])
        L.get_texts()[2].set_text('Curva ROC - média micro (Á'+ L.get_texts()[2].get_text()[-11:])
        L.get_texts()[3].set_text('Curva ROC - média macro (Á'+ L.get_texts()[3].get_text()[-11:])
        plt.savefig(file_path) 
        file_path = os.path.join(results_folder_path, 'PR_curve.png')
        plot_precision_recall_curve(y_true=results['true_labels'], 
                        y_probas=results['predictions_probs'],
                        title='Curvas Precisão-Recall')
        plt.xlabel('Recall')
        plt.ylabel('Precisão')
        L=plt.legend()
        L.get_texts()[0].set_text('Curva precisão-recall - "Não contém agressão" (Á'+ L.get_texts()[0].get_text()[-12:])
        L.get_texts()[1].set_text('Curva precisão-recall - "Contém agressão" (Á'+ L.get_texts()[1].get_text()[-12:])
        L.get_texts()[2].set_text('Curva precisão-recall - média micro (Á'+ L.get_texts()[2].get_text()[-12:])
        plt.savefig(file_path) 


def clear_dir(dir_path:str):
    for fname in os.listdir(dir_path):
        file_path = os.path.join(dir_path, fname)
        os.remove(file_path)

    