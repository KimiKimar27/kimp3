from calculate2 import encode_size

def construct_header(tag_frames: list) -> bytes:
  size = encode_size(len(b"".join(tag_frames)))
  header = bytes()
  header += "ID3".encode("utf-8")       # TAG identifier
  header += b"\x03\x00"                 # TAG version
  header += b"\x00"                     # Flags
  header += size.to_bytes(4, "big")     # Size of TAG
  return header

def construct_frame(identifier: str, content: str) -> bytes:
  content = b"\x00" + content.encode("utf-8")
  size = len(content)
  header = bytes()
  header += identifier.encode("utf-8")  # Frame identifier
  header += size.to_bytes(4, "big")     # Size of frame
  header += b"\x00\x00"                 # Flags
  return header + content

def construct_frames(frames: dict) -> list:
  tag_frames = []
  for identifier, content in frames.items():
    tag_frames.append(construct_frame(identifier, content))
  return tag_frames

def merge_data(header: bytes, frames: list) -> str:
  return header + b"".join(frames)

frames = {
  "TRCK": "1",
  "TCON": "Rock",
  "COMM": "Epic song", # i ne radi bas
  "TYER": "2017",
  "TALB": "Science Fiction",
  "TPE1": "Brand New",
  "TIT2": "Can't Get It Out"
}

tag_frames = construct_frames(frames)

tag_header = construct_header(tag_frames)

metadata = merge_data(tag_header, tag_frames)

with open("mdata.bin", "wb") as f:
  f.write(metadata)