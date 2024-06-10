from . import cat_epub

def main():
    from argparse import ArgumentParser
    from pathlib import Path
    import glob
    import logging

    parser = ArgumentParser()
    parser.add_argument('--input','-i', required=True, action='append')
    args = parser.parse_args()

    inputs = []
    if any('*' not in input for input in args.input):
        inputs = list(map(Path,args.input))
    else:
        for inp in args.inputs:
            if '*' in inp:
                # escape ?, [, and ], but not star
                dodged_glob = glob.glob(glob.escape(args.input.replace('*','@')).replace('@','*'))
                inputs.extend(map(Path,dodged_glob))
            else:
                inppath = Path(inp)
                if inppath.is_file():
                    inputs.append(inppath)
                elif inppath.is_dir():
                    inputs.extend(inppath.rglob('*.epub'))
                else:
                    continue

    for input in inputs:
        try:
            for line in cat_epub(input):
                print(line)
        except KeyboardInterrupt:
            logging.info("User Interrupt. Exiting...")
            raise SystemExit(0)

if __name__ == "__main__":
    main()
