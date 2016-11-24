
// NewsCollectorDlg.cpp : implementation file
//

#include "stdafx.h"
#include "NewsCollector.h"
#include "NewsCollectorDlg.h"
#include "TPCollectorsEdit.h"
#include "Python.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


struct TPCollector 
{
	CString m_sName;
	CString m_sStartUrl;
};
typedef CArray<TPCollector ,TPCollector &> TPCollectorArray;

TPCollectorArray g_aCollector;




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

	TPCollector stuCollector;
	stuCollector.m_sName = _T("网易新闻");
	stuCollector.m_sStartUrl = _T("");

	g_aCollector.RemoveAll();
	g_aCollector.Add(stuCollector);

	CComboBox *pComboBox = (CComboBox*)GetDlgItem(IDC_COMBO_COLLECTOR);
	for (int l = 0 ; l < g_aCollector.GetSize(); l ++)
	{
		pComboBox->AddString(g_aCollector[l].m_sName);
	}
	if(g_aCollector.GetSize() > 0)
	{
		pComboBox->SetCurSel(0);
		GetDlgItem(IDC_EDIT_URL)->SetWindowText(g_aCollector[0].m_sStartUrl);
	}
	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CNewsCollectorDlg::OnCbnSelchangeComboCollector()
{
	CComboBox *pComboBox = (CComboBox*)GetDlgItem(IDC_COMBO_COLLECTOR);

	int iIndex = pComboBox->GetCurSel();
	if(iIndex < g_aCollector.GetSize() && iIndex > 0)
	{
		GetDlgItem(IDC_EDIT_URL)->SetWindowText(g_aCollector[iIndex].m_sStartUrl);
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

char* WideChartoAnsi(wchar_t * pWideChar)
{
	if (NULL == pWideChar)
		return NULL;
	char* pAnsi = NULL;
	int needBytes = WideCharToMultiByte(CP_ACP,0,pWideChar,-1, NULL,0, NULL, NULL);
	if (needBytes >0)
	{
		pAnsi = new char[needBytes + 1];
		ZeroMemory(pAnsi, needBytes + 1);
		WideCharToMultiByte(CP_ACP, 0, pWideChar, -1, pAnsi,needBytes, NULL, NULL);
	}
	return pAnsi;
}
wchar_t* MultiByteToWide(char* pMultiChar)
{
	if (!pMultiChar)
		return NULL;
	wchar_t* pWideBuf = NULL;
	int needWideBytes = MultiByteToWideChar(CP_ACP, 0, pMultiChar, -1, NULL, NULL);
	if (needWideBytes >0)
	{
		pWideBuf = new wchar_t[needWideBytes + 1];
		ZeroMemory(pWideBuf, (needWideBytes+1) * sizeof(wchar_t));
		MultiByteToWideChar(CP_ACP, 0, pMultiChar, -1, pWideBuf, needWideBytes);
	}
	return pWideBuf;
}
void CNewsCollectorDlg::OnBnClickedButton1()
{
	CString sUrl = _T("");
	GetDlgItem(IDC_EDIT_URL)->GetWindowText(sUrl);

	PyObject* pName = NULL;
	PyObject* pModule =NULL;
	PyObject* pDict = NULL;
	PyObject* pFunc = NULL;
	PyObject* pArgs = NULL;
	PyObject* pRet = NULL;
	// 初始化Python

	// 在使用Python系统前，必须使用Py_Initialize对其

	// 进行初始化。它会载入Python的内建模块并添加系统路

	// 径到模块搜索路径中。这个函数没有返回值，检查系统

	// 是否初始化成功需要使用Py_IsInitialized。

	Py_Initialize();

	// 检查初始化是否成功

	Py_IsInitialized();

	// 添加当前路径

	// 把输入的字符串作为Python代码直接运行，返回

	// 表示成功，-1表示有错。大多时候错误都是因为字符串

	// 中有语法错误。
	PyRun_SimpleString("import sys");
	PyRun_SimpleString("sys.path.append('./')");

	// 载入名为PyPlugin的脚本
	pName = PyString_FromString("PyPluginTest");
	pModule = PyImport_Import(pName);
	if (!pModule)
	{
		//printf("can't findPyPlugin.py\n");
	}
	pDict = PyModule_GetDict(pModule);
	if (!pDict)
	{
	}
	// 找出函数名为AddMult的函数
	pFunc = PyDict_GetItemString(pDict, "AddMult");
	if (!pFunc || !PyCallable_Check(pFunc))
	{
		//printf("can't findfunction [AddMult]\n");
	}
	pArgs = Py_BuildValue("ii", 12, 14);
	pRet = PyEval_CallObject(pFunc,pArgs);
	int a = 0;
	int b = 0;
	if (pRet && PyArg_ParseTuple(pRet,"ii", &a,&b))
	{
		//printf("Function[AddMult] call successful a + b = %d, a * b = %d\n", a, b);
		//nRet = 0;
	}
	if (pArgs)
		Py_DECREF(pArgs);
	if (pFunc)
		Py_DECREF(pFunc);

	// 找出函数名为HelloWorld的函数
	pFunc = PyDict_GetItemString(pDict, "HelloWorld");
	if (!pFunc || !PyCallable_Check(pFunc))
	{
		//printf("can't findfunction [HelloWorld]\n");
	}
	CString sJc1 = _T("jc1"),sJc2 = _T("jc2");
	PyObject *pyParams = PyTuple_New(2);  
	PyObject *py1 = PyString_FromString(WideChartoAnsi(sJc1.GetBuffer()));  
	PyObject *py2 = PyString_FromString(WideChartoAnsi(sJc2.GetBuffer()));  
	PyTuple_SetItem(pyParams, 0, py1);  
	PyTuple_SetItem(pyParams, 1, py2);  
	// ok, call the function    
	PyObject *pyResult = PyObject_CallObject(pFunc, pyParams);  
	if(pyResult)  
	{  
		char* pRe =PyString_AsString(pyResult);
		CString sRe = MultiByteToWide(pRe);
		AfxMessageBox(sRe);
	}

	//if (pRet)
	//	Py_DECREF(pRet);
	//if (pArgs)
	//	Py_DECREF(pArgs);
	//if (pFunc)
	//	Py_DECREF(pFunc);
	//if (pDict)
	//	Py_DECREF(pDict);
	//if (pModule)
	//	Py_DECREF(pModule);
	//if (pName)
	//	Py_DECREF(pName);
	Py_Finalize();
}
