import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(color_codes=True)
sns.set(rc={'figure.figsize':(16, 6)})

colors = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'orange',
    4: 'purple'
}

def plot_consumption(df, rae_filter, datetime_filter, datetime_value=None):
    """
    Affiche la consommation d'un batiment (identifié par son id RAE)
    Au choix : par an, sur un moins, une semaine ou un jour
    """
    df_rae = df[df.RAE == rae_filter]
    
    if datetime_filter == "year":
        df_final = df_rae
    elif datetime_filter == "month":
        df_final = df_rae[df_rae.Date.dt.month == datetime_value]
    elif datetime_filter == "week":
        df_final = df_rae[df_rae.Date.dt.weekofyear == datetime_value]
    else:
        df_final = df_rae[df_rae.Date.dt.dayofyear == datetime_value]
    
    sns.lineplot(x="Date", y="kWh", hue="RAE", data=df_final).set_title(
                f"Consumption of {df_rae['NOM DU SITE'].values[0]} in a {datetime_filter}")


def subplot_consumption_by_type(df_labels, df_data, label, date_filters):
    """
    Affiche 4 graphes de consommation par types de batiments
    (Administration, Prison, Ecole...)
    """

    i = 1
    plt.subplots_adjust(hspace=0.5)
    for rae in df_labels[df_labels.Label == label].sample(4, random_state=42).RAE:
        plt.subplot(2, 2, i)   
        plot_consumption(df_data, rae, *date_filters)
        plt.xticks(rotation=30)
        i+=1



def plot_day_clustering(daily_cons, rae_names, cluster_labels):
    """
    Affiche la consommation des 20 premiers jours
    avec la couleur de leur cluster
    """
    n_clusters = len(np.unique(cluster_labels))
    l = len(daily_cons[0])
    plt.subplots_adjust(hspace=0.6)
    for j in range(len(rae_names)):
        plt.subplot(len(rae_names), 1, j+1)
        
        for i in range(20):
            plt.plot(np.
            arange(l*i + l*365*j, l*(i+1) + l*365*j),
                     daily_cons[i + 365*j], c=colors[cluster_labels[i + 365*j]])
            plt.title(f"20 jours de consommation de {rae_names[j]} séparés en {n_clusters} catégories")

            # Remove x axis legend
            frame1 = plt.gca()
            frame1.axes.xaxis.set_ticklabels([])


def plot_types_in_cluster(clusters, true_labels, cluster_id, df_labels):
    """
    Affiche la proportion de chaque type de batiment dans un cluster
    Pour un type, sa proportion est le nombre de ce type dans le cluster
    divisé par le nombre total de ce type dans le dataset.
    """
    values, counts = np.unique(true_labels[np.argwhere(clusters == cluster_id).reshape(-1)],
                    return_counts=True)
    
    sorted_label_counts = df_labels[df_labels.Label.isin(values)].Label.value_counts().sort_index().values
    
    sns.barplot(x=values, y=counts/sorted_label_counts,
                order=values[np.argsort(counts/sorted_label_counts)[::-1]]).set_title(
                f"Proportion de batiment dans le cluster {cluster_id}")