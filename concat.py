import os
import hydra
import pandas as pd
from omegaconf import DictConfig


@hydra.main(version_base="1.2", config_path="configs", config_name="config.yaml")
def main(config: DictConfig = None) -> None:
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
    playlists_df.to_csv(os.path.join(file_path, config.pl_concat), index=False)

    songs_df = pd.concat(songs)
    songs_df.to_csv(os.path.join(file_path, config.song_concat), index=False)


if __name__ == "__main__":
    main()
