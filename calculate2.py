def encode_size(unencoded_value: int) -> int:
  """
  encodes an integer to 4 bytes, where each byte's MSB is 0
  this means that the highest possible integer is 28-bit
  """
  bytes=[]
  encoded_value = ""
  for i in range(0, 4):
    mask = int("1"*(7+i*8), 2) # mask out the bits that arrent getting shifted
    bytes.insert(0, (unencoded_value & mask) >> 8*i) # append byte to beggining of array to keep them in the correct order
    unencoded_value = (unencoded_value & ~mask) << 1 # shift the unmasked bits by one position
  for i in bytes:
    i = bin(i)[2:] # convert int to bytes and remove the leading '0b'
    encoded_value += f"{i:0>8}" # append the byte to the encoded value, filling in the necessary zeroes to make it 8 bits long
  return int(encoded_value, 2)

if __name__ == "__main__":
  print(f"{bin(encode_size(57_724_813))[2:]:0>32}")