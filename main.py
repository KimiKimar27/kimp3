class kimp3():

  def __init__(self, file_path):
    self.file_path   = file_path
    self._TAG_header = kimp3._read_TAG_header(self)
    self._TAG_frames = kimp3._read_TAG_frames(self)
    self._parse_TAG_frames()

  def _read_TAG_header(self):
    TAG_header = {}
    with open(self.file_path, "rb") as f:
      TAG_header["tag_identifier"] = f.read(3)
      TAG_header["tag_version"]    = f.read(2)
      TAG_header["flags"]          = f.read(1)
      TAG_header["size"]           = f.read(4)
      TAG_header["int_size"]  = int.from_bytes(TAG_header["size"])

    return TAG_header

  def _read_TAG_frames(self):
    TAG_frames = {}
    bytes_seeked = 0
    i = 0
    with open(self.file_path, "rb") as f:
      f.seek(10)
      while(bytes_seeked < self._TAG_header["int_size"]):
        TAG_frames[f"frame_{i}"] = {}
        TAG_frames[f"frame_{i}"]["frame_identifier"] = f.read(4)
        TAG_frames[f"frame_{i}"]["size"]             = f.read(4)
        TAG_frames[f"frame_{i}"]["flags"]            = f.read(2)
        TAG_frames[f"frame_{i}"]["int_size"]         = int.from_bytes(TAG_frames[f"frame_{i}"]["size"])
        TAG_frames[f"frame_{i}"]["content"]          = f.read(TAG_frames[f"frame_{i}"]["int_size"])
        bytes_seeked += 10 + TAG_frames[f"frame_{i}"]["int_size"]
        i += 1

      return TAG_frames

  def _parse_TAG_frames(self):
    for frame in self._TAG_frames.values():
      content = frame["content"].decode("utf-8").lstrip("\x00")
      match frame["frame_identifier"].decode("utf-8"):
        case "TRCK":
          self.track_number = content
        case "TENC":
          pass
        case "WXXX":
          pass
        case "TCOP":
          pass
        case "TOPE":
          pass
        case "TCOM":
          pass
        case "TCON":
          self.genre = content
        case "COMM":
          pass
        case "TYER":
          pass
        case "TALB":
          self.album = content
        case "TPE1":
          self.artist = content
        case "TIT2":
          self.song_name = content
        case _:
          raise Exception(f"Unknown frame identifier: {frame['frame_identifier']}")



  ### DEBUG METHODS ###
  def print_TAG_header(self):
    for k, v in self._TAG_header.items():
      print(f"{k}: {v}")

  def print_TAG_frames(self):
    for frame, content in self._TAG_frames.items():
      print(frame, ":")
      for k, v in content.items():
        print(f"\t{k}: {v}")

  def print_properties(self):
    print(f"Track number: {self.track_number}")

def main():
  a = kimp3("ex.mp3")
  print(a.artist)

if __name__ == "__main__":
  main()