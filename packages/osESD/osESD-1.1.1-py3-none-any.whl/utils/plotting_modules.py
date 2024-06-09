import matplotlib.pyplot as plt

def save_plot(data_path, column_name, df, save_path, model_name):
    fig, ax = plt.subplots()
    l = ax.plot(df['timestamps'], df['value'])
    IS = df[df[column_name] > 0]
    ax.plot(IS['timestamps'], IS['value'], "ro")
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("Value")
    ax.set_title(column_name + '_plot')
    plt.savefig(fname=save_path + data_path[:-4] +'_'+ model_name + '.png')
    plt.close()
