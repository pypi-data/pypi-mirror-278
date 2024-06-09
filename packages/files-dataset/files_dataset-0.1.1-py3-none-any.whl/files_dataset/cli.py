from argparse import ArgumentParser

def main():

  parser = ArgumentParser(description="Images Dataset CLI. Creates meta.json files")

  parser.add_argument('COMMAND', choices=['meta'], help='meta: Create a meta.json file')
  parser.add_argument('-a', '--archive', type=str, required=True, help='Relative path (or glob) to the archive file(s)/folder(s)')
  parser.add_argument('-n', '--num-files', type=int, default=None, help='Number of images in the archive')
  parser.add_argument('-f', '--format', choices=['auto', 'zip', 'tar', 'none'], default='auto', help='Format of the archive. If auto, it will be inferred from the file extension. If none, it will be treated as a folder')

  args = parser.parse_args()

  from files_dataset.meta import Meta

  if args.format == 'none':
    format = None
  elif args.format == 'auto':
    if args.archive.endswith('.zip'):
      format = 'zip'
    elif args.archive.endswith('.tar'):
      format = 'tar'
    else:
      format = None
  else:
    format = args.format

  if format is None:
    name = args.archive
  else:
    import os
    name = os.path.splitext(os.path.basename(args.archive))[0]

  archive = Meta.Archive(archive=args.archive, format=format, num_files=args.num_files)
  meta = Meta(files_dataset={ name: archive })
  print(meta.model_dump_json(indent=2))