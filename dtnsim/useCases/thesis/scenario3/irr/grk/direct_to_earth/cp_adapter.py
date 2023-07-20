import pandas as pd

nodes = {"gs": [1, 2, 3],
        "ls": [x for x in range(4, 24)],
        "lr": [24, 25, 26, 27, 28]}


def adapt(fileName):

    file = fileName + '.csv'
    originalCP = pd.read_csv(file)

    data = []
    for idx, row in originalCP.iterrows():

        src = row['SourceEid']
        dst = row['DestinEid']
        
        # keep inter relay links
        if src in nodes["lr"] and dst in nodes["lr"]:
            data.append(row)

        # keep relay to/from earth links
        elif src in nodes["lr"] and dst in nodes["gs"]:
            data.append(row)
        
        elif src in nodes["gs"] and dst in nodes["lr"]:
            data.append(row)

        # keep direct LS <-> GS links
        elif src in nodes["ls"] and dst in nodes["gs"]:
            data.append(row)
        elif src in nodes["gs"] and dst in nodes["ls"]:
            data.append(row)

        # keep region links
        elif src in nodes["ls"]:

            # north stations (90-15)
            if src in [4, 6, 8, 10, 14, 18, 19, 20]:
                if dst in [25, 26]:
                    data.append(row)

            # circ stations (15-(-15))
            if src in [7, 8, 11, 12, 15, 16]:
                if dst == 24:
                    data.append(row)
            
            # south stations ((-15) - (-90))
            if src in [5, 9, 13, 17, 21, 22, 23]:
                if dst in [27, 28]:
                    data.append(row)

        elif dst in nodes["ls"]:

            # north stations (90-15)
            if dst in [4, 6, 8, 10, 14, 18, 19, 20]:
                if src in [25, 26]:
                    data.append(row)

            # circ stations (15-(-15))
            if dst in [7, 8, 11, 12, 15, 16]:
                if src == 24:
                    data.append(row)
            
            # south stations ((-15) - (-90))
            if dst in [5, 9, 13, 17, 21, 22, 23]:
                if src in [27, 28]:
                    data.append(row)

    adaptedCP = pd.DataFrame(data=data, columns=originalCP.columns)
    adaptedCP.to_csv(fileName+'_adapted.csv', index=False)

for type in ["a", "b"]:
    for day in ["1", "2", "3", "4"]:
        fileName = '{}/{}/scenario3_{}_{}'.format(type, day, type, day)
        adapt(fileName)