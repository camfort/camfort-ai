import json
import sys

def split_one_record(record):
    mode = 0
    out = []
    inp = []
    for line in record:
        if line.strip() == '"""':
            mode = 0
        elif mode == 0:
            if line.startswith('Input:'):
                mode = 1
            elif line.startswith('Output:'):
                mode = 2
        elif mode == 1:
            inp.append(line)
        elif mode == 2:
            out.append(line)
    return inp, out

def to_json_line(inp, out):
    return json.dumps({'prompt': ''.join(inp), 'completion': ''.join(out)+'\n!=end\n'})

def main():
    record = []
    for line in sys.stdin:
        if line.strip() == '###':
            inp, out = split_one_record(record)
            print(to_json_line(inp, out))
            record = []
        else:
            record.append(line)

if __name__ == '__main__':
    main()
