__all__ = ['plot_cd_evolution']

# Standard library imports
import pathlib
from pathlib import Path

# Third party imports
import xlrd
import pandas as pd
import matplotlib.pyplot as plt

def plot_cd_evolution(ctg_path:pathlib.WindowsPath)->pd.DataFrame:
    def getBGColor(book, sheet, row, col):
        xfx = sheet.cell_xf_index(row, col)
        xf = book.xf_list[xfx]
        bgx = xf.background.pattern_colour_index
        pattern_colour = book.colour_map[bgx]
    
        return pattern_colour
    
    def addlabels(x,y,z):
            for i in range(len(y)):
                plt.text(x[i],i,z[i],size=15)
    
    file = ctg_path / Path(r'REUNION AG\DATA\Commité directeur\Membre_CD_2014-2024.xls')
    workbook = xlrd.open_workbook(file, formatting_info=True)
    worksheet = workbook.sheet_by_name('CD')
    dic_col = {}
    dic_col [(255, 128, 128)]='reconduit'
    dic_col [(204, 204, 255)]= 'nouveau'
    dic_col [(192, 192, 192)]= 'non_present'
    dic_col [(0, 255, 0) ]= 'reelu'
    dic_col [(255, 0, 0)]= 'demissionnaire'
    
    nrow = worksheet.nrows
    ncolumn = worksheet.ncols
    cd = {}
    cdt = {}
    for col in range(1,ncolumn):
        year = int(worksheet.cell_value(0,col))
        n = 0
        entrant = 0
        dem = 0
        reelu = 0
        for row in range(1,nrow):
            c = getBGColor(workbook, worksheet,  row,col)
    
            if dic_col[c] in ['reconduit','nouveau','reelu']:
                n += 1
            if dic_col[c] == 'nouveau':
                entrant += 1
            if dic_col[c] == 'demissionnaire':
               dem += 1
            if dic_col[c] =='reelu':
               reelu += 1
        cd[year] = [n,entrant,dem]
        cdt[year] = [n,entrant,dem,reelu]
    for year, val in cd.items():
        if year == 2013:
            cd[year]=cd[year]+[0]
        else:
            cd[year]=cd[year]+[n_year_1-val[0] + val[1] - val[2]]
        n_year_1 = val[0]
    df = pd.DataFrame(cd)
    df = df.T
    dg = pd.DataFrame(cdt)
    dg = dg.T
    df.columns = ["# membres","# entrants","# démissions","# sortants"]
    dg.columns = ["# membres","# nouvaux entrants","# démissions","# reelus"]
    df["# démissions"] = -df["# démissions"]
    df["# sortants"] = -df["# sortants"]
    df["# membres année précédente"] = df["# membres"] - df["# entrants"]
    ax =  df.plot(
                  y=["# membres année précédente","# entrants","# démissions","# sortants"],
                  kind='barh',
                  stacked=True,color=['g','y','r','m'],
                  xlim=[-7,25],
                  figsize=(5,10))
    
    ax.grid('on', which='minor', axis='x' )
    ax.grid('on', which='major', axis='x' )
    ax.legend(bbox_to_anchor=(1.0,1.0))
    ax.tick_params(axis='x', rotation=0, labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    df['fac renouvellement'] = 50*(df["# entrants"]-df["# sortants"]-df["# démissions"]) /df["# membres"]
    addlabels(df["# membres"].tolist(),
               df.index.tolist(),
               [f' {round(x,1)} %' for x in df['fac renouvellement'].tolist()])

    return dg
