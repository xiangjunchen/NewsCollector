
// NewsCollectorDlg.cpp : implementation file
//

#include "stdafx.h"
#include "NewsCollector.h"
#include "NewsCollectorDlg.h"
#include "TPCollectorsEdit.h"
#include "TPCollectorData.h"
#include "TPVcPython.h"

extern TPCollectorArray g_aCollector;

#ifdef _DEBUG
#define new DEBUG_NEW
#endif





// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	enum { IDD = IDD_ABOUTBOX };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

// Implementation
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
END_MESSAGE_MAP()


// CNewsCollectorDlg dialog




CNewsCollectorDlg::CNewsCollectorDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CNewsCollectorDlg::IDD, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CNewsCollectorDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CNewsCollectorDlg, CDialog)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	//}}AFX_MSG_MAP
	ON_BN_CLICKED(IDC_BUTTON2, &CNewsCollectorDlg::OnBnClickedButton2)
	ON_CBN_SELCHANGE(IDC_COMBO_COLLECTOR, &CNewsCollectorDlg::OnCbnSelchangeComboCollector)
	ON_BN_CLICKED(IDC_BUTTON1, &CNewsCollectorDlg::OnBnClickedButton1)
	ON_WM_DESTROY()
	ON_BN_CLICKED(IDC_BUTTON3, &CNewsCollectorDlg::OnBnClickedButton3)
END_MESSAGE_MAP()


// CNewsCollectorDlg message handlers

BOOL CNewsCollectorDlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon

	// TODO: Add extra initialization here

	pCollectorData = new CTPCollectorData;
	CComboBox *pComboBox = (CComboBox*)GetDlgItem(IDC_COMBO_COLLECTOR);
	for (int l = 0 ; l < g_aCollector.GetSize(); l ++)
	{
		pComboBox->AddString(g_aCollector[l]->m_sName);
	}
	if(g_aCollector.GetSize() > 0)
	{
		pComboBox->SetCurSel(0);
		GetDlgItem(IDC_EDIT_URL)->SetWindowText(g_aCollector[0]->m_sStartUrl);
	}
	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CNewsCollectorDlg::OnCbnSelchangeComboCollector()
{
	CComboBox *pComboBox = (CComboBox*)GetDlgItem(IDC_COMBO_COLLECTOR);

	int iIndex = pComboBox->GetCurSel();
	if(iIndex < g_aCollector.GetSize() && iIndex > 0)
	{
		GetDlgItem(IDC_EDIT_URL)->SetWindowText(g_aCollector[iIndex]->m_sStartUrl);
	}
}

void CNewsCollectorDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CNewsCollectorDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this function to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CNewsCollectorDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}


void CNewsCollectorDlg::OnBnClickedButton2()
{
	CTPCollectorsEdit editDlg;
	editDlg.DoModal();
}


void CNewsCollectorDlg::OnBnClickedButton1()
{
	CString sUrl = _T("");
	GetDlgItem(IDC_EDIT_URL)->GetWindowText(sUrl);

	CTPVcPython cVcPython;
	//cVcPython.ProcPythonDemo();
	CString sCurrent = cVcPython.CollectorFromUrl(sUrl);
	CString sOutput;
	GetDlgItem(IDC_EDIT_COLLECTORSTATUS)->GetWindowText(sOutput);
	if(!sOutput.IsEmpty())
		sOutput += _T("\r\n");
	sOutput += _T("\r\n");
	sOutput += sCurrent;
	GetDlgItem(IDC_EDIT_COLLECTORSTATUS)->SetWindowText(sOutput);
	((CEdit*)GetDlgItem(IDC_EDIT_COLLECTORSTATUS))->SetSel(-1,-1);
	GetDlgItem(IDC_EDIT_COLLECTORSTATUS)->SetFocus();
}

void CNewsCollectorDlg::OnDestroy()
{
	CDialog::OnDestroy();

	delete pCollectorData;
	pCollectorData = NULL;
	// TODO: Add your message handler code here
}

void CNewsCollectorDlg::OnBnClickedButton3()
{
	GetDlgItem(IDC_EDIT_COLLECTORSTATUS)->SetWindowText(_T(""));
}
