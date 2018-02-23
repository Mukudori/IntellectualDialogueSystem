from PyQt5.QtWidgets import QTableView


def GetSelectedRecordID(tableView):
    currentDiscount = tableView.currentIndex()
    id = tableView.model().data(tableView.model().index(currentDiscount.row(), 0), 0)
    if id:
        return [int(id),currentDiscount]
    else:
        return [0,0]
