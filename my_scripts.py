import json
import argparse as ap

def list_all_data(sorted: str | None):
    with open("Data_base.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    parser = ap.ArgumentParser(description="Da_blya_bot")

    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("list", help="list all user activity data")
    add_parser.add_argument("--sorted_f_name", "-s_fn", help="sorted by name")
    add_parser.add_argument("--sorted_s_name", "-s_sn", help="Adds an ammount")

    upd_parser = subparsers.add_parser("update", help="Updates an existing expense")
    upd_parser.add_argument("ID", help="Expense ID to update")
    upd_parser.add_argument("--description", "-d", default=None, help="Changes description")
    upd_parser.add_argument("--ammount", "-a", default=None, help="Changes ammount")

    del_parser = subparsers.add_parser("del", help="Deletes expense by ID")
    del_parser.add_argument("ID", help="Expense ID to delete")

    args = parser.parse_args()
        