#####################################################################################################################

import numpy as np
import polars as pl
import matplotlib.pyplot as plt 
import seaborn as sns

#####################################################################################################################

def clustering_MDS_plot_one_method(X_mds, y_pred, y_true, title='', accuracy=None, time=None, figsize=(8, 5), bbox_to_anchor=(1.2, 1), 
                        title_size=13, title_weight='bold', points_size=45, title_height=0.98, subtitles_size=12, subtitle_weight='bold',
                        hspace=0.8, wspace=0.4, save=False, file_name=None, legend_size=9):
    """
    Computes and display the MDS plot for a considered clustering configuration, 
    differentiating the cluster labels and the real groups, if they are known.

    Parameters (inputs)
    ----------
    X_mds: a numpy array with the MDS matrix for the distance matrix used in the considered clustering configuration.
    y_pred: a numpy array with the predictions of the response.
    y_true: a numpy array with the true values of the response.
    title: the title of the plot.
    accuracy: the accuracy of the clustering algorithm, if computed.
    time: the execution time of the clustering algorithm, if computed.
    figsize: the size of the plot.
    bbox_to_anchor: the size of the legend box.
    title_fontsize: the size of the font of the title.
    title_weight: the weight of the title.
    points_size: the size of the points of the plot.
    title_height: the height of the tile of the plot.

    Returns (outputs)
    -------
    The described plot.
    """

    X_mds_df = pl.DataFrame(X_mds)
    X_mds_df.columns = ['Z1', 'Z2']
    labels_df = pl.DataFrame(y_pred)
    labels_df.columns = ['cluster_labels']
    MDS_cluster_df = pl.concat((X_mds_df, labels_df), how='horizontal')
    
    if y_true is not None:

        Y_df = pl.DataFrame(y_true)
        Y_df.columns = ['Y']
        MDS_true_df = pl.concat((X_mds_df, Y_df), how='horizontal')

        fig, axes = plt.subplots(1,2, figsize=figsize)
        axes = axes.flatten()
        sns.scatterplot(x='Z1', y='Z2', hue='Y', data=MDS_true_df, ax=axes[0], s=points_size, palette='bright')
        sns.scatterplot(x='Z1', y='Z2', hue='cluster_labels', data=MDS_cluster_df, ax=axes[1], s=points_size, palette='bright')
        axes[0].set_title('Real groups', fontsize=subtitles_size, weight=subtitle_weight)
        if accuracy != None and time != None:
            axes[1].set_title(f'Predicted groups (Acc:{np.round(accuracy,3)}, Time:{np.round(time,1)} secs)', fontsize=subtitles_size, weight=subtitle_weight)
        elif accuracy != None:
            axes[1].set_title(f'Predicted groups (Acc:{np.round(accuracy,3)})', fontsize=subtitles_size, weight=subtitle_weight)
        elif time != None:
            axes[1].set_title(f'Predicted groups (Time:{np.round(time,1)} secs)', fontsize=subtitles_size, weight=subtitle_weight)
        else:
            axes[1].set_title(f'Predicted groups', fontsize=11)
        axes[0].legend(title='Y', bbox_to_anchor=bbox_to_anchor, loc='upper right', fontsize=legend_size)
        axes[1].legend(title='Cluster\nlabels',bbox_to_anchor=bbox_to_anchor, loc='upper right', fontsize=legend_size)
        plt.subplots_adjust(hspace=hspace, wspace=wspace) 
        plt.suptitle(title, fontsize=title_size, y=title_height, weight=title_weight, color='black')

    else:

        fig, axes = plt.subplots(figsize=figsize)
        ax = sns.scatterplot(x='Z1', y='Z2', hue='cluster_labels', data=MDS_cluster_df, s=points_size, palette='bright')
        ax.set_title(title, fontsize=title_size, y=title_height, weight=title_weight, color='black')
        ax.legend(title='Cluster\nlabels', bbox_to_anchor=bbox_to_anchor, loc='upper right', fontsize=legend_size)
 
    if save == True:
        fig.savefig(file_name, format='jpg', dpi=500, bbox_inches="tight", pad_inches=0.2)
    plt.show()

#####################################################################################################################

def clustering_MDS_plot_multiple_methods(X_mds, y_pred, y_true, title='', accuracy=None, time=None, n_rows=2, figsize=(8, 5), bbox_to_anchor=(1.2, 1), 
                        title_size=13, title_weight='bold', points_size=45, title_height=0.98, subtitles_size=12, subtitle_weight='bold',
                        hspace=0.8, wspace=0.4, save=False, file_name=None, legend_size=9):
    """
    Computes and display the MDS plot for a considered clustering configuration, 
    differentiating the cluster labels and the real groups, if they are known.

    Parameters (inputs)
    ----------
    X_mds: a numpy array with the MDS matrix for the distance matrix used in the considered clustering configuration.
    y_pred: a numpy array with the predictions of the response.
    y_true: a numpy array with the true values of the response.
    title: the title of the plot.
    accuracy: the accuracy of the clustering algorithm, if computed.
    time: the execution time of the clustering algorithm, if computed.
    figsize: the size of the plot.
    bbox_to_anchor: the size of the legend box.
    title_fontsize: the size of the font of the title.
    title_weight: the weight of the title.
    points_size: the size of the points of the plot.
    title_height: the height of the tile of the plot.

    Returns (outputs)
    -------
    The described plot.
    """
    
    MDS_cluster_df = {}
    X_mds_df = pl.DataFrame(X_mds)
    X_mds_df.columns = ['Z1', 'Z2']
    methods = y_pred.keys()
    for method in methods:
        labels_df = pl.DataFrame(y_pred[method])
        labels_df.columns = ['cluster_labels']
        MDS_cluster_df[method] = pl.concat((X_mds_df, labels_df), how='horizontal')
    
    Y_df = pl.DataFrame(y_true)
    Y_df.columns = ['Y']
    MDS_true_df = pl.concat((X_mds_df, Y_df), how='horizontal')

    n_methods = len(methods)
    n_cases = n_methods + 1
    n_cols = int(np.ceil(n_cases / n_rows))

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten()
    
    sns.scatterplot(x='Z1', y='Z2', hue='Y', data=MDS_true_df, ax=axes[0], s=points_size, palette='bright')
    axes[0].set_title('Real groups', fontsize=subtitles_size, weight=subtitle_weight)
    axes[0].legend(title='Y', bbox_to_anchor=bbox_to_anchor, loc='upper right', fontsize=legend_size)

    for i, method in enumerate(methods):

        sns.scatterplot(x='Z1', y='Z2', hue='cluster_labels', data=MDS_cluster_df[method], ax=axes[i+1], s=points_size, palette='bright')

        if accuracy != None and time != None:
            axes[i+1].set_title(f'Predicted groups by {method}\n Acc:{np.round(accuracy[method],3)} - Time:{np.round(time[method],1)} secs', fontsize=subtitles_size, weight=subtitle_weight)
        elif accuracy != None:
            axes[i+1].set_title(f'Predicted groups by {method}\n Acc:{np.round(accuracy[method],3)}', fontsize=subtitles_size, weight=subtitle_weight)
        elif time != None:
            axes[i+1].set_title(f'Predicted groups by {method}\n Time:{np.round(time[method],1)} secs', fontsize=subtitles_size, weight=subtitle_weight)
        else:
            axes[i+1].set_title(f'Predicted groups by {method}\n ', fontsize=11)
        axes[i+1].legend(title='Cluster\nlabels', bbox_to_anchor=bbox_to_anchor, loc='upper right', fontsize=legend_size)

    plt.subplots_adjust(hspace=hspace, wspace=wspace) 
    plt.suptitle(title, fontsize=title_size, y=title_height, weight=title_weight, color='black')
    for j in range(n_cases, n_rows * n_cols):
        fig.delaxes(axes[j])
    if save == True:
        fig.savefig(file_name, format='jpg', dpi=500, bbox_inches="tight", pad_inches=0.2)
    plt.show()

#####################################################################################################################

def clustering_MDS_plot(X_mds, y_pred, y_true, title='', accuracy=None, time=None, figsize=(8, 5), n_rows=2, bbox_to_anchor=(1.2, 1), 
                        title_size=13, title_weight='bold', points_size=45, title_height=0.98, subtitles_size=12, subtitle_weight='bold',
                        hspace=0.8, wspace=0.4, save=False, file_name=None, legend_size=9):
    
    if isinstance(y_pred, dict):

        clustering_MDS_plot_multiple_methods(X_mds=X_mds, y_pred=y_pred, y_true=y_true, title=title, accuracy=accuracy, time=time, n_rows=n_rows, figsize=figsize, 
                                             bbox_to_anchor=bbox_to_anchor, title_size=title_size, title_weight=title_weight, points_size=points_size, 
                                             title_height=title_height, subtitles_size=subtitles_size, subtitle_weight=subtitle_weight,
                                             hspace=hspace, wspace=wspace, save=save, file_name=file_name, legend_size=legend_size)
    
    else:

        clustering_MDS_plot_one_method(X_mds=X_mds, y_pred=y_pred, y_true=y_true, title=title, accuracy=accuracy, time=time, figsize=figsize, 
                                        bbox_to_anchor=bbox_to_anchor, title_size=title_size, title_weight=title_weight, points_size=points_size, 
                                        title_height=title_height, subtitles_size=subtitles_size, subtitle_weight=subtitle_weight,
                                        hspace=hspace, wspace=wspace, save=save, file_name=file_name, legend_size=legend_size)

#####################################################################################################################

def clustering_MDS_multiplot(X_mds, y_pred, n_cols, title='', figsize=(8, 5), bbox_to_anchor=(1.2, 1), 
                        title_fontsize=13, subtitle_size=11, legend_size=9, title_weight='bold', points_size=45, title_height=0.98,
                        hspace=0.5, wspace=0.5):
    """
    Computes and display a multi-plot with the MDS plots for different clustering configurations.

    Parameters (inputs)
    ----------
    X_mds: a dictionary with the MDS matrix of the distance matrices used in each considered clustering configuration.
    y_pred: a dictionary with the clustering labels of each configuration and with the same keys of `X_mds`.
    title: the title of the plot.
    accuracy: the accuracy of the clustering algorithm, if computed.
    time: the execution time of the clustering algorithm, if computed.
    figsize: the size of the plot.
    bbox_to_anchor: the size of the legend box.
    title_fontsize: the size of the font of the title.
    title_weight: the weight of the title.
    points_size: the size of the points of the plot.
    title_height: the height of the tile of the plot.
    subtitle_size: size of the title of the subplots.
    legend_size: size of the legend.
    hspace: amount of height between subplots.
    wspace: amount of width between subplots.

    Returns (outputs)
    -------
    The described plot.
    """    
    
    cases = X_mds.keys()
    n_cases = len(cases)
    MDS_cluster_df = {}

    for key in cases:

        X_mds_df = pl.DataFrame(X_mds[key])
        X_mds_df.columns = ['Z1', 'Z2']
        labels_df = pl.DataFrame(y_pred[key])
        labels_df.columns = ['cluster_labels']
        MDS_cluster_df[key] = pl.concat((X_mds_df, labels_df), how='horizontal')
    
    n_rows = int(np.ceil(n_cases/n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten()  

    for i, key in enumerate(cases):

        sns.scatterplot(x='Z1', y='Z2', hue='cluster_labels', data=MDS_cluster_df[key], 
                        s=points_size, palette='bright', ax=axes[i])
        axes[i].set_title(key, fontsize=subtitle_size)
        axes[i].legend(title='Clusters\nlabels', bbox_to_anchor=bbox_to_anchor, loc='upper right', fontsize=legend_size)

    plt.suptitle(title, fontsize=title_fontsize, y=title_height, weight=title_weight, color='black')
    plt.subplots_adjust(hspace=hspace, wspace=wspace) 

    plt.show() 