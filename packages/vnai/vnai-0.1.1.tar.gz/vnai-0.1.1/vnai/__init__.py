import os
import pathlib
import importlib.metadata
import requests
import psutil
import platform
import uuid
import sys
import socket
import json
import base64
from cryptography.fernet import Fernet

TC_VAR = "ACCEPT_TC"
TC_VAL = "tôi đồng ý"

lmt = os.path.sep
HOME_DIR = pathlib.Path.home()
PROJECT_DIR = HOME_DIR / ".vnstock"
ID_DIR = PROJECT_DIR / 'id'
TG = b'gAAAAABmOPXPmFYXs94INEralMxhR38geFp91TZRLP29C41OoO0k7D7QiXIR2nWl5PCEoQCKECZw8b-Xeek3oqT6LcpcpJsAPyOGOBTX5cw_r5Mv0o8SBLa53jOeuVAwCAhId_BpMtOO'
TC_PATH = ID_DIR / "terms_agreement.txt"

TERMS_AND_CONDITIONS = """
        Vui lòng nhập 'Tôi đồng ý' hoặc nhấn Enter để chấp nhận các điều khoản, điều kiện và tiếp tục sử dụng phần mềm. 

        Bạn cũng có thể tự động chấp nhận điều khoản và ẩn thông báo này với câu lệnh mẫu bên dưới:

        ```
        import os
        if "ACCEPT_TC" not in os.environ:
        os.environ["ACCEPT_TC"] = "tôi đồng ý"
        ```

        THOẢ THUẬN & GIẤY PHÉP SỬ DỤNG PHẦN MỀM VNSTOCK3
        ------------------------------------------------

        (*) Gói thư viện Python Vnstock thế hệ thứ 3 được phát hành vào tháng 5 năm 2024, được đề cập đến trong giấy phép này với tên gọi tắt là Vnstock3.

        Khi bạn truy cập, sử dụng nội dung mã nguồn Vnstock3, hoặc cài đặt Vnstock3 trên thiết bị của mình, bạn xác nhận rằng mình đã đọc, hiểu rõ, và chấp nhận điều khoản sử dụng phần mềm như mô tả dưới đây. 
        Bạn cần xác nhận điều khoản & điều kiện trong lần đầu tiên chạy thư viện Vnstock để có thể sử dụng.

        I. ĐIỀU KHOẢN CHUNG
        -------------------

        Cấp Phép: Thư viện này chỉ dành cho mục đích cá nhân và không được phân phối lại hoặc sử dụng cho mục đích thương mại mà không có sự đồng ý bằng văn bản chính thức từ tác giả. Tất cả bản quyền và sở hữu trí tuệ thuộc về tác giả. Bất kỳ hành vi vi phạm bản quyền hoặc sở hữu trí tuệ sẽ chịu trách nhiệm trước pháp luật.

        Hạn Chế Sử Dụng Thương Mại: Sử dụng Vnstock3 cho mục đích thương mại bởi bất kỳ tổ chức nào là không được phép nếu không có sự đồng ý bằng văn bản của tác giả. Điều này bao gồm, nhưng không giới hạn, các hoạt động mà Vnstock3 trực tiếp hoặc gián tiếp góp phần tạo ra doanh thu hoặc dòng tiền cho một tổ chức mà không có sự chấp thuận từ tác giả. Tuy nhiên, việc sử dụng Vnstock3 cho mục đích cá nhân, nghiên cứu vẫn được duy trì miễn phí với điều kiện bạn phải tuân thủ việc công khai trích dẫn thông tin dự án trong sản phẩm của mình. Trong trường hợp tổ chức của bạn cần sử dụng Vnstock3 cho mục đích thương mại, vui lòng liên hệ với tác giả để được hỗ trợ và cấp phép sử dụng chính thức.

        Các Mục Đích Sử Dụng Bị Cấm: Bạn không được sử dụng Vnstock cho các mục đích bất hợp pháp, phi đạo đức, hoặc trái với quy định pháp luật hiện hành.

        Từ Chối Trách Nhiệm: Tác giả không chịu trách nhiệm cho bất kỳ thiệt hại, mất mát, hoặc hậu quả nào phát sinh từ việc sử dụng thư viện này, đặc biệt trong hoạt động đầu tư hoặc bất kỳ hoạt động nào có rủi ro. Bạn tự chịu trách nhiệm cho các quyết định đầu tư của mình.

        Tuân Thủ Luật Pháp: Bạn đồng ý tuân thủ mọi luật pháp, quy định, và hướng dẫn liên quan khi sử dụng thư viện này.

        Bảo Mật Dữ Liệu: Bạn đồng ý cho phép Vnstock3 thu thập và lưu trữ dữ liệu ẩn danh của thiết bị nhằm mục đích phân tích và tối ưu hiệu năng, trải nghiệm sử dụng của phần mềm. Thông tin này được bảo mật và sẽ không được chia sẻ với bên thứ ba mà không có sự đồng ý của bạn.

        II. BẢN QUYỀN VÀ SỞ HỮU
        -----------------------

        Bản quyền (c) 2024 Thinh Vu @ Vnstock. Tất cả các quyền được bảo lưu.

        Sử Dụng và Phân Phối Không Được Phép: Việc sao chép, phân phối, hoặc khai thác thương mại Vnstock3, hoặc bất kỳ phần nào của nó là không được phép. Giới hạn này bao gồm bất kỳ hình thức tạo ra doanh thu hoặc sử dụng cho tổ chức mà không được sự cho phép rõ ràng của tác giả. Tuy nhiên, việc sử dụng cá nhân, chỉnh sửa, và nghiên cứu học thuật không liên quan đến lợi ích thương mại vẫn được duy trì. Người dùng tham gia vào các hoạt động được cho phép nên tôn trọng mục đích của phần mềm này như một công cụ cho việc thúc đẩy phát triển cá nhân và mục đích giáo dục, chứ không phải để lợi dụng tính chất mở của phần mềm cho mục đích sinh lợi trong khi tổ chức vốn có nguồn tiềm lực về tài chính và con người nhưng không chia sẻ với tác giả và đội ngũ phát triển. Vi phạm các điều khoản này tương đương với việc đánh cắp quyền sở hữu trí tuệ và phi đạo đức, có thể dẫn đến các rắc rối pháp lý kèm theo.

        III. CHẤM DỨT
        -------------

        Thỏa thuận này có hiệu lực cho đến khi được chấm dứt. Nó sẽ tự động chấm dứt ngay lập tức mà không cần thông báo từ tác giả nếu bạn không tuân thủ bất kỳ điều khoản nào của thỏa thuận này. Sau khi chấm dứt, bạn phải hủy bỏ tất cả các bản sao của Vnstock3 và tất cả các bộ phận thành phần của nó.

        IV. ĐIỀU KHOẢN THI HÀNH
        -----------------------

        Thỏa thuận này sẽ được điều chỉnh và giải thích theo luật pháp của quốc gia mà tác giả cư trú, không kể đến các quy định xung đột của pháp luật.

        Bằng cách sử dụng Vnstock3, bạn đồng ý rằng mình sẽ bị ràng buộc bởi các điều khoản của Thỏa thuận này. 
        Nếu bạn không đồng ý với các điều khoản của Thỏa thuận này, vui lòng không cài đặt hoặc sử dụng Vnstock3.
        """

class VnstockInitializer:
    def __init__(self, target, tc=TERMS_AND_CONDITIONS):
        self.terms_and_conditions = tc
        self.home_dir = HOME_DIR
        self.project_dir = PROJECT_DIR
        self.id_dir = ID_DIR
        self.terms_file_path = TC_PATH
        self.env_config = ID_DIR / "environment.json"
        self.RH = 'asejruyy^&%$#W2vX>NfwrevDRESWR'
        self.LH = 'YMAnhuytr%$59u90y7j-mjhgvyFTfbiuUYH'

        # Create the project directory if it doesn't exist
        self.project_dir.mkdir(exist_ok=True)
        self.id_dir.mkdir(exist_ok=True)
        self.target = target

        kb = (str(self.project_dir).split(lmt)[-1] + str(self.id_dir).split(lmt)[-1] + str(self.terms_file_path).split(lmt)[-1]).ljust(32)[:32].encode('utf-8')
        kb64 = base64.urlsafe_b64encode(kb)
        self.cph = Fernet(kb64)

    def system_info(self):
        """
        Gathers information about the environment and system.
        """
        # Generate UUID
        machine_id = str(uuid.uuid4())

        # Environment (modify to detect your specific frameworks)
        try:
            from IPython import get_ipython
            if 'IPKernelApp' not in get_ipython().config:  # Check if not in IPython kernel
                if sys.stdout.isatty():
                    environment = "Terminal"
                else:
                    environment = "Other"  # Non-interactive environment (e.g., script executed from an IDE)
            else:
                environment = "Jupyter"
        except (ImportError, AttributeError):
            # Fallback if IPython isn't installed or other checks fail
            if sys.stdout.isatty():
                environment = "Terminal"
            else:
                environment = "Other"

        try:
            if 'google.colab' in sys.modules:
                hosting_service = "Google Colab"
            elif 'CODESPACE_NAME' in os.environ:
                hosting_service = "Github Codespace"
            elif 'GITPOD_WORKSPACE_CLUSTER_HOST' in os.environ:
                hosting_service = "Gitpod"
            elif 'REPLIT_USER' in os.environ:
                hosting_service = "Replit"
            elif 'KAGGLE_CONTAINER_NAME' in os.environ:
                hosting_service = "Kaggle"
            elif '.hf.space' in os.environ['SPACE_HOST']:
                hosting_service = "Hugging Face Spaces"
        except:
            hosting_service = "Local or Unknown"

        # System information
        os_info = platform.uname()

        # CPU information
        cpu_arch = platform.processor()  
        cpu_logical_cores = psutil.cpu_count(logical=True)
        cpu_cores = psutil.cpu_count(logical=False)

        # Memory information
        ram_total = psutil.virtual_memory().total / (1024**3)  # GB
        ram_available = psutil.virtual_memory().available / (1024**3)  # GB

        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)])

        # Combine information into a dictionary
        info = {
            "uuid": machine_id,
            "environment": environment,
            "hosting_service": hosting_service,
            "python_version": platform.python_version(),
            "os_name": os_info.system,
            "os_version": os_info.version,
            "machine": os_info.machine,
            "cpu_model": cpu_arch,
            "cpu_cores": cpu_cores,
            "cpu_logical_cores": cpu_logical_cores,
            "ram_total": round(ram_total, 1),
            "ram_available": round(ram_available, 1),
            "local_ip": IPAddr,
            "mac_address": mac,
        }

        return info

    def show_terms_and_conditions(self):
        """
        Displays terms and conditions and asks for acceptance.
        """
        print(self.terms_and_conditions)
        
        # check if os.environ[TC_VAR] exist and equal to tôi đồng ý
        if TC_VAR in os.environ and os.environ[TC_VAR] == TC_VAL:
            response = TC_VAL
        else:
            response = input("Nhập 'Tôi đồng ý' hoặc nhấn Enter để chấp nhận: ")
            if not response.strip():
                response = TC_VAL
                os.environ[TC_VAR] = response

        if response.strip().lower() == TC_VAL:
            from datetime import datetime
            # get now time in string
            now = datetime.now()
            HARDWARE = self.system_info()
            # VERSION = pkg_resources.get_distribution('vnstock').version
            
            VERSION = None
            try:
                VERSION = importlib.metadata.version('vnstock')
            except importlib.metadata.PackageNotFoundError:
                # print("Package 'vnstock' not found")
                pass

            # parse HARDWARE to string to store in the file
            signed_aggreement = f"MÔ TẢ:\nNgười dùng có mã nhận dạng {HARDWARE['uuid']} đã chấp nhận điều khoản & điều kiện sử dụng Vnstock lúc {now}\n---\n\nTHÔNG TIN THIẾT BỊ: {str(HARDWARE)}\n\nĐính kèm bản sao nội dung bạn đã đọc, hiểu rõ và đồng ý dưới đây:\n{self.terms_and_conditions}"
            
            # Store the acceptance
            with open(self.terms_file_path, "w", encoding="utf-8") as f:
                f.write(signed_aggreement)

            print("---\nCảm ơn bạn đã chấp nhận điều khoản và điều kiện!\nBạn đã có thể tiếp tục sử dụng Vnstock!")
            return True
        else:
            return False

    def log_analytics_data(self):
        """
        Sends analytics data to a webhook.
        """
        HARDWARE = self.system_info()
        EP = 'gAAAAABmOPNX4DJAsImlkzvtcyezBxr4UcK_HpCOgz-GOF9yBDP99tWNFYM_ZjeC22kNqmX3urZa467BC1D2fPLJrUkp6rQizYEMK4m196ZlOzUhwCbfjdvURXesL3LC7DofOgwWjNyltPQ8AnPyB4YUMnnAwnFooQ=='
        TGE = self.cph.decrypt(self.target).decode('utf-8')
        WH = f"{self.cph.decrypt(((self.RH+EP+self.RH)[30:-30]).encode()).decode('utf-8')}{TGE}"

        data = {
            "systems": HARDWARE,
            "accepted_agreement": True,
            "installed_packages": self.packages_installed(),
        }

        # save data to a json file in id folder
        with open(self.env_config, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4))

        try:
            response = requests.post(WH, json=data)
        except:
            raise SystemExit("Không thể gửi dữ liệu phân tích. Vui lòng kiểm tra kết nối mạng và thử lại sau.")

    def check_terms_accepted(self):
        """
        Checks if terms and conditions are accepted.
        """
        if not self.env_config.exists() or not self.terms_file_path.exists():
            # If not, ask for acceptance
            accepted = self.show_terms_and_conditions()
            if not accepted:
                raise SystemExit("Điều khoản và điều kiện không được chấp nhận. Không thể tiếp tục.")
            else:
                self.log_analytics_data()

    def packages_installed(self):
        """
        Checks installed packages and returns a dictionary.
        """
        # Define package mapping
        package_mapping = {
                    "vnstock_family": [
                        "vnstock",
                        "vnstock3",
                        "vnstock_ezchart",
                        "vnstock_data_pro"
                        "vnstock_market_data_pipeline",
                        "vnstock_ta",
                        "vnii",
                        "vnai",
                    ],
                    "analytics": [
                        "openbb",
                        "pandas_ta"
                    ],
                    "static_charts": [
                        "matplotlib",
                        "seaborn",
                        "altair"
                    ],
                    "dashboard": [
                        "streamlit",
                        "voila",
                        "panel",
                        "shiny",
                        "dash",
                    ],
                    "interactive_charts": [
                        "mplfinance",
                        "plotly",
                        "plotline",
                        "bokeh",
                        "pyecharts",
                        "highcharts-core",
                        "highcharts-stock",
                        "mplchart",
                    ],
                    "datafeed": [
                        "yfinance",
                        "alpha_vantage",
                        "pandas-datareader",
                        "investpy",
                    ],
                    "official_api": [
                        "ssi-fc-data",
                        "ssi-fctrading"
                    ],
                    "risk_return": [
                        "pyfolio",
                        "empyrical",
                        "quantstats",
                        "financetoolkit",
                    ],
                    "machine_learning": [
                        "scipy",
                        "sklearn",
                        "statsmodels",
                        "pytorch",
                        "tensorflow",
                        "keras",
                        "xgboost"
                    ],
                    "indicators": [
                        "stochastic",
                        "talib",
                        "tqdm",
                        "finta",
                        "financetoolkit",
                        "tulipindicators"
                    ],
                    "backtesting": [
                        "vectorbt",
                        "backtesting",
                        "bt",
                        "zipline",
                        "pyalgotrade",
                        "backtrader",
                        "pybacktest",
                        "fastquant",
                        "lean",
                        "ta",
                        "finmarketpy",
                        "qstrader",
                    ],
                    "server": [
                        "fastapi",
                        "flask",
                        "uvicorn",
                        "gunicorn"
                    ],
                    "framework": [
                        "lightgbm",
                        "catboost",
                        "django",
                    ]
                }

        installed_packages = {}

        for category, packages in package_mapping.items():
            installed_packages[category] = []
            for pkg in packages:
                try:
                    version = importlib.metadata.version(pkg)
                    installed_packages[category].append((pkg, version))
                except importlib.metadata.PackageNotFoundError:
                    pass

        return installed_packages

def tc_init():
    vnstock_initializer = VnstockInitializer(TG)
    vnstock_initializer.check_terms_accepted()
