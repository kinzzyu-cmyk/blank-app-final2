import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(page_title="개념 기반 탐구 SNA 분석", layout="wide")
st.title("💡 패션디자인 전공 학생들의 개념 기반 탐구 의미망(SNA) 분석")
st.markdown("특성화고 학생들의 에듀테크 협업 및 찬반 토론 전후의 사고 확장 과정 시각화")

# 2. 사이드바 설정 (데이터 전환 버튼)
st.sidebar.header("분석 시점 선택")
data_choice = st.sidebar.radio(
    "어떤 네트워크를 확인하시겠습니까?",
    ("탐구 초기 (T1) - 단편적 현상 중심", "탐구 후기 (T2) - 가치 및 개념 융합 중심")
)

# 3. 네트워크 생성 함수
def create_network_graph(data_choice):
    # 빈 그래프 생성
    G = nx.Graph()
    
    # 데이터 세트 정의 (이전 단계에서 추출한 노드와 가중치)
    if "T1" in data_choice:
        # 탐구 초기 데이터
        edges = [
            ("디지털 의류", "메타버스", 2), ("디지털 의류", "정체성", 2), 
            ("메타버스", "정체성", 1), ("생성형 AI", "디자인 권위", 2), 
            ("생성형 AI", "저작권", 1), ("생성형 AI", "창의성", 2), 
            ("디자인 권위", "창의성", 1), ("3D 시뮬레이션", "장인정신", 1), 
            ("3D 시뮬레이션", "지속가능성", 1), ("3D 시뮬레이션", "정체성", 2), 
            ("장인정신", "정체성", 1), ("리셀 시장", "MZ세대", 2), 
            ("리셀 시장", "과시적 소비", 1), ("리셀 시장", "문화", 2), 
            ("MZ세대", "문화", 1), ("AI 가상 피팅", "신체 긍정", 2), 
            ("AI 가상 피팅", "관점", 2), ("신체 긍정", "관점", 1), 
            ("문화적 전유", "전통 복식", 1), ("문화적 전유", "현대적 재해석", 1), 
            ("문화적 전유", "문화", 2), ("전통 복식", "창의성", 1), 
            ("버추얼 인플루언서", "브랜드 메시지", 2), ("버추얼 인플루언서", "소통", 2), 
            ("브랜드 메시지", "소통", 1), ("패스트 패션", "환경 오염", 2), 
            ("패스트 패션", "패션 민주화", 1), ("패스트 패션", "재현", 2), 
            ("환경 오염", "재현", 1), ("젠더리스", "사회적 역할", 2), 
            ("젠더리스", "변화", 2), ("사회적 역할", "변화", 1)
        ]
        color_scheme = "#A0C4FF" # T1은 파란색 톤
    else:
        # 탐구 후기 데이터
        edges = [
            ("정체성", "디지털 패션", 4), ("정체성", "상호작용", 3), 
            ("정체성", "비물질성", 2), ("창의성", "생성형 AI", 5), 
            ("창의성", "예술적 가치", 4), ("창의성", "인간 주체성", 3), 
            ("관점", "친환경 패션", 4), ("관점", "윤리적 소비", 3), 
            ("관점", "환경 보호", 5), ("관점", "정당한 비용", 2), 
            ("변화", "생성형 AI", 4), ("변화", "패션 산업", 3), 
            ("변화", "가치 평가", 2), ("생성형 AI", "디지털 패션", 3), 
            ("친환경 패션", "환경 보호", 4), ("윤리적 소비", "환경 보호", 3), 
            ("예술적 가치", "인간 주체성", 2)
        ]
        color_scheme = "#FFADAD" # T2는 붉은색/따뜻한 톤 (사고의 융합)

    # 엣지 및 노드 추가
    for source, target, weight in edges:
        G.add_edge(source, target, value=weight, title=f"연결 강도: {weight}")

    # Pyvis 네트워크 설정
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    
    # NetworkX 그래프를 Pyvis로 변환
    net.from_nx(G)

    # 노드 크기 및 색상 디자인 적용
    for node in net.nodes:
        node['size'] = 15 + (len(list(G.neighbors(node['id']))) * 5) # 연결선이 많을수록 노드 크기 증가
        node['color'] = color_scheme
        node['font'] = {'size': 20, 'face': 'pretendard'}

    # 물리 엔진 설정 (노드들이 자연스럽게 밀어내도록 설정)
    net.repulsion(node_distance=150, spring_length=200)

    # HTML 파일로 저장 후 읽어오기
    try:
        path = '/tmp'
        net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')
    except:
        net.save_graph('pyvis_graph.html')
        HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')
        
    source_code = HtmlFile.read()
    return source_code

# 4. 화면에 그래프 렌더링
st.subheader(data_choice)
html_content = create_network_graph(data_choice)
components.html(html_content, height=650)

# 5. 하단 교육적 해석 추가
st.markdown("---")
if "T1" in data_choice:
    st.info("**분석 결과 (탐구 초기)**: '메타버스', '생성형 AI' 등 산업의 표면적 기술/현상 키워드가 중심을 차지하며, 핵심 개념어(정체성, 창의성 등)는 파편화되어 개별 현상에 단순 연결되어 있습니다.")
else:
    st.success("**분석 결과 (탐구 후기)**: '창의성', '관점' 등 인문학적 개념어들이 네트워크 중심부로 이동하여 여러 단어들을 매개하며, '환경 보호', '인간 주체성' 등 고차원적인 진로 철학 키워드로 사고가 확장(융합)되었습니다.")
