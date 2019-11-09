식질머신
========
<sup>[English](README.md) | 한국어</sup>

![szmc-0.1.0](doc/szmc-0.1.0.gif)
<sup>(출처: [manga109](http://www.manga109.org), © Kanno Hiroshi, © Okuda Momoko, © Kato Masaki)</sup>

식질머신은 식자 작업에서 **글자 제거 작업**을 **자동화**합니다.
</br></br>

![SeisinkiVulnus_028](doc/1.jpg)

![LoveHina_vol14_003](doc/2.jpg)

![AkkeraKanjinchou_031](doc/3.jpg)
위 이미지들은 모두 사람의 개입 없이 자동으로 편집되었습니다.\
<sup>(출처: [manga109](http://www.manga109.org), © Shimazaki Yuzuru, © Akamatsu Ken, © Kobayashi Yuki)</sup>

~어케했누
-----

### 모델

![szmc-structure-kor](doc/szmc-structure-kor.png)

식질머신은 만화에서 텍스트를 찾아내고, 자연스럽게 지워냅니다.\
두 과정 모두 사람의 개입 없이 **완전히 자동으로 진행**됩니다.\
물론 원한다면 지우고 싶은 영역을 지정할 수도 있습니다.

SegNet으로 [U-net](https://arxiv.org/abs/1505.04597)을 적용했고, ComplNet으로 [Deepfill v2](http://jiahuiyu.com/deepfill2/)를 적용했습니다.

### 데이터셋
식질머신은 SegNet과 ComplNet 두개의 딥러닝 모델로 이루어집니다. 

**SegNet** 학습을 위해서는 **원본 만화 이미지**와 \
원본에 대응하여 텍스트,효과음 영역을 가리키는 **텍스트 컴포넌트 마스크**가 필요합니다. 

**ComplNet** 학습을 위해서는 **텍스트가 제거된 만화 이미지**(즉, **출력**)가 필요합니다. \
(텍스트가 약간 존재하는 이미지가 성능에 얼마나 영향을 미치는지는 연구 중입니다. \
 텍스트가 전혀 존재하지 않는 만화 이미지가 가장 이상적인 데이터이긴 합니다.)
 
0.1.1 버전은 이미지-마스크 285 쌍과 31,497개의 만화 이미지를 이용하여 학습하였습니다. \
(31,497개의 만화 이미지 중 11,464개는 텍스트가 존재하는 이미지입니다.)
 
식질머신에 데이터셋을 기여하고 싶으시다면 <a href="mailto:kur.creative.org@gmail.com">이메일</a>로 데이터를 보내주시면 됩니다. \
데이터셋은 오직 연구 목적으로만 이용될 것입니다.


Release
-----
**현재 0.1.1 pre-release 버전을 배포하고 있습니다!** \
[여기서 다운로드할 수 있습니다.](https://github.com/KUR-creative/SickZil-Machine/releases) \
[사용방법과 팁](https://github.com/KUR-creative/SickZil-Machine/blob/master/doc/tips/tips-0.1.1-kor.md)

현재 식질머신은 완벽하지 않습니다. 사용자 여러분의 도움이 필요합니다. \
혹시 버그를 발견하셨거나 제안이 있으시다면 [깃헙 이슈](https://github.com/KUR-creative/SickZil-Machine/issues)를 열어 제보해 주시거나 <a href="mailto:kur.creative.org@gmail.com">이메일</a>을 보내주세요.\
특히 이슈의 경우, 영어를 모르시면 그냥 한국어로 쓰셔도 됩니다.    

Run the code(for developers)
----

NVIDIA driver 410.x, CUDA 10.0, CUDNN (>= 7.4.1)이 필요합니다(텐서플로우 1.13.0 요구사항).

0. `git clone https://github.com/KUR-creative/SickZil-Machine.git; cd SickZil-Machine`
1. [여기](https://github.com/KUR-creative/SickZil-Machine/releases)서 릴리즈 빌드 중 하나를 다운로드합니다.
2. 압축을 풀고 `SickZil-Machine-0.1.1-pre0-win64-cpu-eng/resource/cnet` 과 `SickZil-Machine-0.1.1-pre0-win64-cpu-eng/resource/snet` 폴더를 `SickZil-Machine/resource`폴더로 복사합니다.
3. `pip install -r requirements.txt`
4. `cd src; python main.py`

Future works
-----
- 만화 텍스트 세그멘테이션 성능 높이기
- 만화 텍스트 세그멘테이션 마스크 데이터셋 공개하기
- "식자" 자동화하기(손글씨 스타일 학습)
