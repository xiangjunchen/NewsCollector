// TPCollectorsEdit.cpp : implementation file
//

#include "stdafx.h"
#include "NewsCollector.h"
#include "TPCollectorsEdit.h"


// CTPCollectorsEdit dialog

IMPLEMENT_DYNAMIC(CTPCollectorsEdit, CDialog)

CTPCollectorsEdit::CTPCollectorsEdit(CWnd* pParent /*=NULL*/)
	: CDialog(CTPCollectorsEdit::IDD, pParent)
{

}

CTPCollectorsEdit::~CTPCollectorsEdit()
{
}

void CTPCollectorsEdit::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}


BEGIN_MESSAGE_MAP(CTPCollectorsEdit, CDialog)
END_MESSAGE_MAP()


// CTPCollectorsEdit message handlers

BOOL CTPCollectorsEdit::OnInitDialog()
{
	CDialog::OnInitDialog();

	// TODO:  Add extra initialization here

	CListCtrl *pListCtrl = GetDlgItem(IDC_LIST_COLLOECTOR);
	return TRUE;  // return TRUE unless you set the focus to a control
	// EXCEPTION: OCX Property Pages should return FALSE
}
