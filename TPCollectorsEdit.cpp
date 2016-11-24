// TPCollectorsEdit.cpp : implementation file
//

#include "stdafx.h"
#include "NewsCollector.h"
#include "TPCollectorsEdit.h"

CString g_sCollectorColum[] = {
	_T("��������"),
	_T("��ʼ��ַ"),
	_T("���һ�βɼ�ʱ��"),
	_T("�ɼ�״̬")
};
// CTPCollectorsEdit dialog

IMPLEMENT_DYNAMIC(CTPCollectorsEdit, CDialog)

CTPCollectorsEdit::CTPCollectorsEdit(CWnd* pParent /*=NULL*/)
	: CDialog(CTPCollectorsEdit::IDD, pParent)
{
	m_pListCtrl = NULL;
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

	m_pListCtrl = (CListCtrl*)GetDlgItem(IDC_LIST_COLLOECTOR);
	for (int l = 0 ; l < sizeof(g_sCollectorColum)/sizeof(CString) ; l++)
	{
		m_pListCtrl->InsertColumn(l, g_sCollectorColum[l],LVCFMT_LEFT,100);
	}
	return TRUE;  // return TRUE unless you set the focus to a control
	// EXCEPTION: OCX Property Pages should return FALSE
}
