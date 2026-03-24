function SongList({ songs, setCurrentSong }) {
  return (
    <div>
      {songs.map((song, index) => (
        <div key={index} onClick={() => setCurrentSong(song)}>
          <h3>{song.song_name}</h3>
          <p>{song.rass}</p>
        </div>
      ))}
    </div>
  );
}

export default SongList;