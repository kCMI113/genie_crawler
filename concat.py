import os
import pandas as pd

if __name__ == "__main__":
    # Concat total file
    file_path = "./outputs/"
    files = [file for file in os.listdir(file_path) if ".csv" in file]
    files = sorted(files, key=lambda x: int(x[: x.find("_")]))

    playlists, songs = [], []
    for file in files:
        if "pl_info" in file:
            playlists.append(pd.read_csv(os.path.join(file_path, file)))
        else:
            songs.append(pd.read_csv(os.path.join(file_path, file)))

    playlists_df = pd.concat(playlists)
    playlists_df.to_csv(os.path.join(file_path, "playlists.csv"), index=False)

    songs_df = pd.concat(songs)
    songs_df.to_csv(os.path.join(file_path, "songs.csv"), index=False)
