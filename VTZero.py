from flask import Flask, request, render_template_string
import asyncio
import vt
import County_Codes
from dotenv import load_dotenv
import os

# .env 파일이 존재하지 않는 경우 생성
if not os.path.exists('.env'):
    api_key = input("Please enter your VirusTotal API key: ")
    with open('.env', 'w') as f:
        f.write(f"API_KEY={api_key}\n")
    print(".env file created successfully.")
else:
    print(".env file already exists.")

# .env 파일에서 환경 변수 로드
load_dotenv()

API_KEY = os.getenv('API_KEY')  # .env 파일에서 API 키 가져오기

if not API_KEY:
    raise ValueError("API_KEY is not set. Please set the API_KEY in the .env file.")

app = Flask(__name__)

TEMPLATE = '''
<!doctype html>
<html>
<head><title>IP Information</title></head>
<body>
    <h1>IP Information</h1>
    <form method="post">
        <textarea name="ips" rows="10" cols="50" placeholder="Enter IPs, one per line"></textarea><br>
        <input type="submit" value="Submit">
    </form>
    {% if results %}
    <h2>Results</h2>
    <table border="1">
        <tr>
            <th>IP</th>
            <th>국가</th>
            <th>소유자</th>
            <th>유해</th>
        </tr>
        {% for ip, info in results.items() %}
        <tr>
            <td>{{ ip }}</td>
            <td>{{ info.country }}</td>
            <td>{{ info.as_owner }}</td>
            <td style="color: {{ 'red' if info.malicious|int >= 1 else 'black' }}">{{ info.malicious }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
</body>
</html>
'''

async def get_ip_info(client, ip):
    result = {'country': '', 'as_owner': '', 'malicious': ''}
    try:
        ip_info = await client.get_object_async(f"/ip_addresses/{ip}")
        ip_info_dict = ip_info.to_dict()  # Object를 dictionary로 변환

        if 'attributes' in ip_info_dict:
            attributes = ip_info_dict['attributes']
            if 'country' in attributes:
                country_code = attributes['country']
                result['country'] = County_Codes.country_code_to_korean.get(country_code, country_code)
            if 'last_analysis_stats' in attributes:
                result['malicious'] = str(attributes['last_analysis_stats']['malicious'])
            if 'as_owner' in attributes:
                result['as_owner'] = attributes['as_owner']
    except Exception as e:
        print(f"Error fetching data for IP {ip}: {e}")
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == 'POST':
        ips = request.form['ips'].split()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = vt.Client(API_KEY)
        tasks = [get_ip_info(client, ip) for ip in ips]
        results_list = loop.run_until_complete(asyncio.gather(*tasks))
        for ip, info in zip(ips, results_list):
            results[ip] = info
        client.close()
    return render_template_string(TEMPLATE, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 모든 IP 주소에서 접근 가능
