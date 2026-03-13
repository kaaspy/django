from local_lib.path import Path

def my_program():
    d = Path("./my_dir")
    if d.exists():
        d.rmtree()
    d.mkdir()
    f = Path("./my_dir/my_file.txt")
    f.write_text("my text in my file")
    print(f.read_text())

if __name__ == "__main__":
    my_program()