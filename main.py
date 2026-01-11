import argparse
from travis_perkins import run

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--page', type=str, default="travis_perkins", help='',
                        choices=['travis_perkins', 'materials_market', 'jewson', 'wickes', 'building_materials'])
    parser.add_argument('--mode', type=str, default="retail", help='', choices=['retail', 'trade'])
    args = parser.parse_args()

    if args.page == "travis_perkins":
        run.main(args.mode)

    elif args.page == "materials_market":
        pass

    elif args.page == "jewson":
        pass

    elif args.page == "wickes":
        pass

    elif args.page == "building_materials":
        pass