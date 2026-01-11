import argparse
import travis_perkins
import materials_market
import jewson
import wickes
import building_materials

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--page', type=str, default="travis_perkins", help='',
                        choices=['travis_perkins', 'materials_market', 'jewson', 'wickes', 'building_materials'])
    parser.add_argument('--mode', type=str, default="retail", help='', choices=['retail', 'trade'])
    args = parser.parse_args()

    if args.page == "travis_perkins":
        travis_perkins.run.main(args.mode)

    elif args.page == "materials_market":
        materials_market.run.main(args.mode)

    elif args.page == "jewson":
        jewson.run.main(args.mode)

    elif args.page == "wickes":
        wickes.run.main(args.mode)

    elif args.page == "building_materials":
        building_materials.run.main(args.mode)