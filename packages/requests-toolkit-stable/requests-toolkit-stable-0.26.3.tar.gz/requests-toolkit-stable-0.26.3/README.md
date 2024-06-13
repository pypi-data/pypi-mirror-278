# requests-toolkit

## Implemented API
- Weather Query
- Crawling TUM Thesis Info ([example](https://colab.research.google.com/drive/1XuznN9ifaac-2WvG470kuJINUbNkyzcv?usp=sharing))
- Academic Query
- Air Quality by Country
- Real Time Exchange Rate (CN)
- RealPython News
- async
- async chatgpt

## Roadmap
- [ ] ...

## Usage
### Install
```bash
pip install requests-toolkit-stable
```

1. python:
  ```python
  #!pip install git+https://github.com/leoxiang66/requests-tutorial.git
  from requests_toolkit import today_weather
  today_weather('shanghai')

  '''
  2022年09月05日, 星期一, 壬寅年八月初十. 上海天气为阴转小雨, 23 ~ 27℃, 湿度：100%, 风向：北风 1级, 紫外线：无, 空气质量：优, PM: 1, 日出: 05:32, 日落: 18:13.

  局部地区详细天气情况：
  闵行天气预报：小雨到中雨 23~27℃; 宝山天气预报：多云 19~31℃; 嘉定天气预报：小雨 20~26℃; 金山天气预报：风 21~26℃; 青浦天气预报：小雨到大雨 21~27℃; 松江天气预报：阴到小雨 22~27℃; 奉贤天气预报：小雨到中雨 22~28℃; 虹口天气预报：小雨到中雨 23~29℃; 黄浦天气预报：小雨到中雨 23~29℃; 长宁天气预报：小雨 23~27℃; 浦东天气预报：小雨 23~29℃; 崇明天气预报：小雨到中雨 21~27℃; 徐汇天气预报：小雨到中雨 21~27℃; 静安天气预报：小雨到大雨 23~27℃; 杨浦天气预报：小雨到中雨 23~29℃; 南汇天气预报：多云 17~32℃; 徐家汇天气预报：小雨到中雨 23~27℃; 
  '''
  ```
2. [web app](https://huggingface.co/spaces/Adapting/weather_query)
