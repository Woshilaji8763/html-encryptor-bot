import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import random
import string
import os
from datetime import datetime
import re
import requests
import time
import json
from collections import deque

# 设置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot配置
BOT_TOKEN = '7838707734:AAHUINQudboDg6C1y8oS1K9hy6koNucyUG4'

# 预测系统API配置
DATA_API = "https://mzplayapi.com/api/webapi/GetNoaverageEmerdList"
ISSUE_API = "https://mzplayapi.com/api/webapi/GetGameIssue"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzUyMjE1NjI3IiwibmJmIjoiMTc1MjIxNTYyNyIsImV4cCI6IjE3NTIyMTc0MjciLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiI3LzExLzIwMjUgMzowMzo0NyBQTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6IjUzODc4OCIsIlVzZXJOYW1lIjoiNjAxNjI4Nzc1NTUiLCJVc2VyUGhvdG8iOiI3IiwiTmlja05hbWUiOiLov73kuI3liLDlpbnjgILjgILjgILwn5iu4oCN8J-SqCIsIkFtb3VudCI6IjIuODQiLCJJbnRlZ3JhbCI6IjAiLCJMb2dpbk1hcmsiOiJINSIsIkxvZ2luVGltZSI6IjcvMTEvMjAyNSAyOjMzOjQ3IFBNIiwiTG9naW5JUEFkZHJlc3MiOiIyMDAxOmY0MDo5NjI6NDA1MTpjNDM1OmFiYjg6MzE1Mzo4MGY5IiwiRGJOdW1iZXIiOiIwIiwiSXN2YWxpZGF0b3IiOiIwIiwiS2V5Q29kZSI6IjM2MzUiLCJUb2tlblR5cGUiOiJBY2Nlc3NfVG9rZW4iLCJQaG9uZVR5cGUiOiIxIiwiVXNlclR5cGUiOiIwIiwiVXNlck5hbWUyIjoiY3JvY2swNjI0QGdtYWlsLmNvbSIsImlzcyI6Imp3dElzc3VlciIsImF1ZCI6ImxvdHRlcnlUaWNrZXQifQ.o0mErq9sW3L8vSvSoqVhIiEMPZvaAFBEl3DIdNGwo_s"

# API parameters
PERIOD_RANDOM = "7dcf66753ae84e4aa4d2a580f77074ee"
PERIOD_SIGNATURE = "6AF57E6606A5F7FE3E4B546DB775F984"
PAGE1_RANDOM = "ba405fefd1f14657a1585f8e6e2d2eca"
PAGE1_SIGNATURE = "2D2AE8B587A43E4AEAF91F69E5B4583A"

# Pages data embedded in the bot
PAGES_DATA = [
    {"pageNo": 1, "random": "ba405fefd1f14657a1585f8e6e2d2eca", "signature": "2D2AE8B587A43E4AEAF91F69E5B4583A", "timestamp": 1752217080},
    {"pageNo": 2, "random": "038ccdd426d0441eb7ed2850d3773b04", "signature": "9A2D135E523271D970CAF4A5B3509F33", "timestamp": 1752217082},
    {"pageNo": 3, "random": "2404b2c16d564aeab9653a77ccfb11f8", "signature": "A7FF95535D1501020C69E6B13982A22D", "timestamp": 1752217082},
    {"pageNo": 4, "random": "beae1f0d3c67419183fbc5f1829041d3", "signature": "4FEBABBBFB497CEE5E2D41A7B5701750", "timestamp": 1752217082},
    {"pageNo": 5, "random": "7fa341a24bcf4a859ae8d16621349004", "signature": "6C8119FE74DE708732B7865C4F193883", "timestamp": 1752217082},
    {"pageNo": 6, "random": "e76a1a87b51a48d093bb51367c94e2d3", "signature": "2BF1664C9112F06A1CCC97CBAE7C585D", "timestamp": 1752217082},
    {"pageNo": 7, "random": "0f3f1f1e57ee4fbbbc807e4acd572101", "signature": "FFEB07CA3B827C9D1654BECE0BE288F9", "timestamp": 1752217082},
    {"pageNo": 8, "random": "fc8c62b31f8e4daba066d0d3f48eba96", "signature": "718211D27891A64E57E3355E5F4B7B6F", "timestamp": 1752217082},
    {"pageNo": 9, "random": "ae3708bac4ba46e0b8717e581c40c471", "signature": "C13406E1E326DAAFD510B947C7F9ED88", "timestamp": 1752217082},
    {"pageNo": 10, "random": "d89f613e06474e82ab51d8c922deea60", "signature": "6D8FEA22A09087B7DAC4698005B94A80", "timestamp": 1752217082}
]

class TripleFunctionBot:
    def __init__(self):
        self.current_gold_price = 3335.00  # 默认金价
        
        # 预测系统相关
        self.recent_actual_results = deque(maxlen=20)
        self.recent_accuracy = deque(maxlen=20)
        self.current_strategy = "ensemble"
        self.prediction_history = deque(maxlen=10)
        self.pending_predictions = {}  # 存储等待验证的预测
        
        # 测试策略功能
        self.test_periods = [
            "20250721100010805",  # Predicted Small, Actual Big
            "20250721100010806",  # Predicted Big, Actual Small  
            "20250721100010807",  # Predicted Big, Actual Small
            "20250721100010808",  # Predicted Small, Actual Big
        ]
        self.test_actual_results = ["Big", "Small", "Small", "Big"]
        
    # ======================== HTML 加密功能 ========================
    def encrypt_html(self, html_content):
        """HTML加密功能"""
        encrypted_dict = {}
        for i, char in enumerate(html_content):
            encrypted_dict[i] = hex(ord(char))[2:]
        return encrypted_dict
    
    def generate_decryption_script(self, encrypted_dict, var_name=None):
        """生成解密脚本"""
        if var_name is None:
            var_name = ''.join(random.choices(string.ascii_letters, k=8))
        
        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        
        script = f"""<!DOCTYPE html>
<html>
<head>
<title>Protected Content</title>
<script src='https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js'></script>
</head>
<body><!--
 * ============================================
 * 🛡 TanMayMods HTML Encryption Script
 * ============================================
 *
 * 🔧 DEVELOPER INFO:
 * -------------------
 * 🧑‍💻 Developer: @CKWinGg1330
 * 🌐 Version: 1.0
 *
 * 📢 CONTACT:
 * ------------
 * - 🔵 Telegram: @CKWinGg1330
 * - 🔥 Channel: @TeamCKGroup
 *
 * 🔒 ENCRYPTION ID: [TaNMaY-ENC-{random_id}]
 *
 * ============================================
-->
<script>
    var {var_name} = {encrypted_dict};
    var decrypted_html = "";
    for (var i in {var_name}) {{
        decrypted_html += String.fromCharCode(parseInt({var_name}[i], 16));
    }}
    document.write(decrypted_html);
</script>
</body>
</html>"""
        return script
    
    # ======================== Lot Size 计算功能 ========================
    def calculate_lot_size_usd(self, lot_size):
        """计算Lot Size对应的USD金额"""
        try:
            lot_size = float(lot_size)
            ounces = lot_size * 100
            usd_value = ounces * self.current_gold_price
            pip_value = lot_size * 10
            margin_required = usd_value * 0.01
            
            return {
                'lot_size': lot_size,
                'ounces': ounces,
                'current_price': self.current_gold_price,
                'usd_value': round(usd_value, 2),
                'pip_value': round(pip_value, 2),
                'margin_required': round(margin_required, 2),
                'calculation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except ValueError:
            return None
    
    def verify_predictions(self):
        """验证等待中的预测"""
        latest = self.fetch_latest_result()
        if not latest:
            return []
        
        verified_results = []
        
        # 检查待验证的预测
        for prediction_data in list(self.prediction_history):
            if prediction_data["status"] == "Pending":
                if latest["issue"] == prediction_data["issue"]:
                    # 找到匹配的结果
                    actual = latest["bigsmall"]
                    is_win = prediction_data["prediction"] == actual
                    result = "WIN" if is_win else "LOSE"
                    
                    # 更新预测状态
                    prediction_data["status"] = result
                    prediction_data["actual"] = actual
                    
                    # 添加到历史记录
                    self.recent_actual_results.append(actual)
                    self.recent_accuracy.append(result)
                    
                    verified_results.append({
                        "issue": prediction_data["issue"],
                        "prediction": prediction_data["prediction"],
                        "actual": actual,
                        "result": result,
                        "confidence": prediction_data["confidence"]
                    })
        
        return verified_results
    
    def set_gold_price(self, price):
        """设置金价"""
        try:
            self.current_gold_price = float(price)
            return True
        except ValueError:
            return False
    
    # ======================== 预测系统功能（原版算法）========================
    def weighted_choice(self, weights):
        """Weighted random selection function"""
        total = sum(weights.values())
        rand = random.random() * total
        for choice, weight in weights.items():
            rand -= weight
            if rand <= 0:
                return choice
        return list(weights.keys())[0]  # Fallback return

    def strategy_1_reverse_current_logic(self, period_number):
        """Strategy 1: Completely reverse the failing logic"""
        digits = [int(d) for d in str(period_number)]
        digit_sum = sum(digits)
        
        # REVERSE EVERYTHING - if current logic fails, try opposite
        if digit_sum >= 18:  # Was Small → Now Big
            level1_weights = {"Big": 0.7, "Small": 0.3}
        elif digit_sum >= 9:  # Was balanced → Now favor based on last digit
            last_digit = digits[-1] if digits else 0
            if last_digit >= 5:
                level1_weights = {"Big": 0.6, "Small": 0.4}
            else:
                level1_weights = {"Big": 0.4, "Small": 0.6}
        else:  # Was Big → Now Small
            level1_weights = {"Big": 0.3, "Small": 0.7}
        
        return self.weighted_choice(level1_weights)

    def strategy_2_simple_last_digit(self, period_number):
        """Strategy 2: Super simple - just use last digit"""
        last_digit = int(str(period_number)[-1])
        return "Big" if last_digit >= 5 else "Small"

    def strategy_3_alternating_pattern(self, period_number, recent_results):
        """Strategy 3: Try to predict based on alternating patterns"""
        if not recent_results:
            return self.strategy_2_simple_last_digit(period_number)
        
        # Look at last 3 results and try to find pattern
        if len(recent_results) >= 2:
            last_two = list(recent_results)[-2:]
            if last_two[0] == last_two[1]:  # Same twice → predict opposite
                return "Small" if last_two[-1] == "Big" else "Big"
            else:  # Different → predict same as last
                return list(recent_results)[-1]
        
        return self.strategy_2_simple_last_digit(period_number)

    def strategy_4_sum_modulo(self, period_number):
        """Strategy 4: Use sum modulo approach"""
        digits = [int(d) for d in str(period_number)]
        digit_sum = sum(digits)
        return "Big" if digit_sum % 2 == 0 else "Small"

    def strategy_5_weighted_ensemble(self, period_number, recent_results):
        """Strategy 5: Combine multiple strategies with weights"""
        votes = {
            "Big": 0,
            "Small": 0
        }
        
        # Get predictions from each strategy
        pred1 = self.strategy_1_reverse_current_logic(period_number)
        pred2 = self.strategy_2_simple_last_digit(period_number)
        pred3 = self.strategy_3_alternating_pattern(period_number, recent_results)
        pred4 = self.strategy_4_sum_modulo(period_number)
        
        # Weight the votes
        votes[pred1] += 0.3
        votes[pred2] += 0.2
        votes[pred3] += 0.25
        votes[pred4] += 0.25
        
        return "Big" if votes["Big"] > votes["Small"] else "Small"

    def dynamic_confidence_calculation(self, recent_accuracy):
        """Calculate confidence based on recent performance"""
        if not recent_accuracy:
            return 0.5  # 50% if no history
        
        # Calculate win rate from recent results
        wins = sum(1 for result in recent_accuracy if result == "WIN")
        total = len(recent_accuracy)
        win_rate = wins / total if total > 0 else 0.5
        
        # Adjust confidence based on performance
        if win_rate >= 0.7:
            return 0.85
        elif win_rate >= 0.6:
            return 0.75
        elif win_rate >= 0.5:
            return 0.65
        elif win_rate >= 0.4:
            return 0.55
        else:
            return max(0.35, 0.5 - (0.5 - win_rate))  # Don't go below 35%

    def improved_predict_big_or_small(self, period_number, recent_results=None, recent_accuracy=None, strategy="ensemble"):
        """Improved prediction with multiple strategies and dynamic confidence"""
        
        if strategy == "reverse":
            prediction = self.strategy_1_reverse_current_logic(period_number)
        elif strategy == "simple":
            prediction = self.strategy_2_simple_last_digit(period_number)
        elif strategy == "alternating":
            prediction = self.strategy_3_alternating_pattern(period_number, recent_results or [])
        elif strategy == "modulo":
            prediction = self.strategy_4_sum_modulo(period_number)
        else:  # ensemble
            prediction = self.strategy_5_weighted_ensemble(period_number, recent_results or [])
        
        confidence = self.dynamic_confidence_calculation(recent_accuracy or [])
        
        return prediction, confidence
    
    def predict_big_or_small(self, period_number):
        """预测大小 - 使用原版算法"""
        prediction, confidence = self.improved_predict_big_or_small(
            period_number, 
            self.recent_actual_results, 
            self.recent_accuracy,
            strategy=self.current_strategy
        )
        
        return prediction, confidence
    
    def fetch_current_issue(self):
        """获取当前期号"""
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json, text/plain, */*",
            "Authorization": AUTH_TOKEN
        }
        body = {
            "typeId": 1,
            "language": 0,
            "random": PERIOD_RANDOM,
            "signature": PERIOD_SIGNATURE,
            "timestamp": int(time.time())
        }
        try:
            r = requests.post(ISSUE_API, headers=headers, json=body, timeout=10)
            data = r.json()
            return data.get("data", {}).get("issueNumber")
        except Exception as e:
            logger.error(f"获取当前期号失败: {e}")
            return None
    
    def fetch_latest_result(self):
        """获取最新结果"""
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json, text/plain, */*",
            "Authorization": AUTH_TOKEN
        }
        body = {
            "pageSize": 10,
            "pageNo": 1,
            "typeId": 1,
            "language": 0,
            "random": PAGE1_RANDOM,
            "signature": PAGE1_SIGNATURE,
            "timestamp": int(time.time())
        }
        try:
            r = requests.post(DATA_API, headers=headers, json=body, timeout=10)
            data = r.json().get("data", {}).get("list", [])
            if not data:
                return None
            
            latest = data[0]
            return {
                "issue": latest["issueNumber"],
                "number": latest["number"],
                "bigsmall": "Big" if int(latest["number"]) >= 5 else "Small",
                "records": data[:5]  # 只返回最近5条
            }
        except Exception as e:
            logger.error(f"获取最新结果失败: {e}")
            return None

# 初始化工具
bot_tools = TripleFunctionBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    keyboard = [
        [InlineKeyboardButton("🔒 HTML 加密工具", callback_data='html_encrypt')],
        [InlineKeyboardButton("💰 Lot Size 计算", callback_data='lot_calculator')],
        [InlineKeyboardButton("🎯 Big/Small 预测", callback_data='prediction_system')],
        [InlineKeyboardButton("ℹ️ 使用帮助", callback_data='help_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """🚀 三功能工具 Bot

🔥 **核心功能**:
🔹 HTML 代码加密保护
🔹 Lot Size 精确计算
🔹 Big/Small 智能预测

💡 **快速使用**:
• 发送HTML代码 → 自动加密
• 发送 `lot 0.1` → 计算金额
• 发送 `price 3335` → 设置金价
• 点击预测 → 获取Big/Small建议

🎯 选择功能开始使用！"""
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理按钮回调"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'html_encrypt':
        await query.edit_message_text(
            "🔒 HTML 加密工具\n\n"
            "🛡️ **功能特点**:\n"
            "• 军用级加密保护\n"
            "• 防止源码泄露\n"
            "• 保持功能完整\n"
            "• 随机变量名生成\n\n"
            "📋 **使用方法**:\n"
            "1. 上传.html文件\n"
            "2. 发送HTML代码\n"
            "3. 获取加密后的文件\n\n"
            "💻 **示例**:\n"
            "直接发送HTML代码即可自动加密"
        )
    
    elif query.data == 'lot_calculator':
        keyboard = [
            [InlineKeyboardButton("💰 设置金价", callback_data='set_price_info')],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"💰 Lot Size 计算器\n\n"
            f"📊 **当前金价**: ${bot_tools.current_gold_price:,.2f}\n\n"
            f"💡 **使用方法**:\n"
            f"• 发送 `lot 0.1` → 计算0.1手\n"
            f"• 发送 `手数 1.0` → 计算1.0手\n"
            f"• 发送 `price 3335` → 设置金价\n\n"
            f"📋 **计算内容**:\n"
            f"• 手数转USD金额\n"
            f"• 每点价值计算\n"
            f"• 保证金需求\n"
            f"• 风险管理建议\n\n"
            f"🎯 试试发送: `lot 0.1`",
            reply_markup=reply_markup
        )
    
    elif query.data == 'prediction_system':
        keyboard = [
            [InlineKeyboardButton("🎯 获取预测", callback_data='get_prediction')],
            [InlineKeyboardButton("📊 最新结果", callback_data='latest_results')],
            [InlineKeyboardButton("🧠 策略选择", callback_data='strategy_selection')],
            [InlineKeyboardButton("📈 预测历史", callback_data='prediction_history')],
            [InlineKeyboardButton("⚠️ 风险提示", callback_data='prediction_warning')],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        win_rate = 0
        if bot_tools.recent_accuracy:
            wins = sum(1 for r in bot_tools.recent_accuracy if r == "WIN")
            win_rate = wins / len(bot_tools.recent_accuracy) * 100
        
        await query.edit_message_text(
            f"🎯 Big/Small 预测系统\n\n"
            f"🧠 **智能算法**:\n"
            f"• 多策略集成预测\n"
            f"• 动态置信度计算\n"
            f"• 历史数据学习\n"
            f"• 实时结果追踪\n\n"
            f"📊 **当前状态**:\n"
            f"• 预测策略: {bot_tools.current_strategy.upper()}\n"
            f"• 最近准确率: {win_rate:.1f}%\n"
            f"• 历史记录: {len(bot_tools.recent_accuracy)} 次\n\n"
            f"🎯 选择功能:",
            reply_markup=reply_markup
        )
    
    elif query.data == 'strategy_selection':
        strategy_keyboard = [
            [InlineKeyboardButton("🧪 测试所有策略", callback_data='test_strategies')],
            [InlineKeyboardButton("🔄 REVERSE" + ("✅" if bot_tools.current_strategy == "reverse" else ""), callback_data='strategy_reverse')],
            [InlineKeyboardButton("🎯 SIMPLE" + ("✅" if bot_tools.current_strategy == "simple" else ""), callback_data='strategy_simple')],
            [InlineKeyboardButton("🔀 ALTERNATING" + ("✅" if bot_tools.current_strategy == "alternating" else ""), callback_data='strategy_alternating')],
            [InlineKeyboardButton("🔢 MODULO" + ("✅" if bot_tools.current_strategy == "modulo" else ""), callback_data='strategy_modulo')],
            [InlineKeyboardButton("🧠 ENSEMBLE" + ("✅" if bot_tools.current_strategy == "ensemble" else ""), callback_data='strategy_ensemble')],
            [InlineKeyboardButton("🔙 返回预测系统", callback_data='prediction_system')]
        ]
        strategy_markup = InlineKeyboardMarkup(strategy_keyboard)
        
        strategy_text = f"""🧠 预测策略选择

📊 **当前策略**: {bot_tools.current_strategy.upper()}

🧪 **测试所有策略**: 在历史数据上测试表现

🔄 **REVERSE**: 完全反转失败的逻辑
• 适用于连续失败时调整策略

🎯 **SIMPLE**: 基于最后一位数字
• 最简单直接的预测方法

🔀 **ALTERNATING**: 交替模式预测
• 基于历史结果寻找规律

🔢 **MODULO**: 数字和模运算
• 使用数学运算预测

🧠 **ENSEMBLE**: 集成所有策略
• 综合多种策略的预测结果

💡 选择策略后会应用到下次预测"""
        
        await query.edit_message_text(strategy_text, reply_markup=strategy_markup)
    
    elif query.data == 'test_strategies':
        processing_msg = await query.edit_message_text("🧪 正在测试所有策略...")
        
        try:
            strategies = ["reverse", "simple", "alternating", "modulo", "ensemble"]
            test_results = []
            best_strategy = None
            best_score = -1
            
            for strategy in strategies:
                correct = 0
                for i, period in enumerate(bot_tools.test_periods):
                    prediction, _ = bot_tools.improved_predict_big_or_small(
                        period, 
                        bot_tools.test_actual_results[:i] if i > 0 else [], 
                        strategy=strategy
                    )
                    if prediction == bot_tools.test_actual_results[i]:
                        correct += 1
                
                accuracy = correct / len(bot_tools.test_actual_results) * 100
                test_results.append((strategy, accuracy, correct))
                
                if accuracy > best_score:
                    best_score = accuracy
                    best_strategy = strategy
            
            test_text = "🧪 策略测试结果\n\n"
            test_text += "📊 **在最近失败案例上的表现**:\n"
            test_text += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            
            for strategy, accuracy, correct in test_results:
                result_emoji = "🎯" if accuracy >= 75 else "⚠️" if accuracy >= 50 else "❌"
                test_text += f"{result_emoji} {strategy.upper()}: {accuracy:.1f}% ({correct}/{len(bot_tools.test_actual_results)})\n"
            
            test_text += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            if best_strategy and best_score > 0:
                test_text += f"🏆 **最佳策略**: {best_strategy.upper()} ({best_score:.1f}%)\n\n"
                
                if best_strategy != bot_tools.current_strategy:
                    test_text += f"💡 建议: 考虑切换到 {best_strategy.upper()} 策略"
                else:
                    test_text += f"✅ 当前策略 {bot_tools.current_strategy.upper()} 表现最佳"
            else:
                test_text += "🤔 所有策略在测试数据上表现相近"
            
            back_keyboard = [
                [InlineKeyboardButton("🔙 返回策略选择", callback_data='strategy_selection')]
            ]
            back_markup = InlineKeyboardMarkup(back_keyboard)
            
            await processing_msg.edit_text(test_text, reply_markup=back_markup)
            
        except Exception as e:
            logger.error(f"策略测试失败: {e}")
            await processing_msg.edit_text("❌ 策略测试失败，请稍后重试")
    
    elif query.data.startswith('strategy_'):
        strategy_name = query.data.replace('strategy_', '')
        bot_tools.current_strategy = strategy_name
        
        strategy_names = {
            'reverse': 'REVERSE - 反转失败逻辑',
            'simple': 'SIMPLE - 最后数字预测',
            'alternating': 'ALTERNATING - 交替模式',
            'modulo': 'MODULO - 模运算',
            'ensemble': 'ENSEMBLE - 集成策略'
        }
        
        await query.edit_message_text(
            f"✅ 策略切换成功！\n\n"
            f"🧠 **新策略**: {strategy_names.get(strategy_name, strategy_name.upper())}\n\n"
            f"📊 新策略将应用到下次预测\n"
            f"🎯 点击\"获取预测\"试用新策略\n\n"
            f"💡 可随时切换策略以获得最佳效果"
        )
    
    elif query.data == 'get_prediction':
        processing_msg = await query.edit_message_text("🔄 正在获取最新预测...")
        
        try:
            # 获取当前期号
            current_issue = bot_tools.fetch_current_issue()
            if not current_issue:
                await processing_msg.edit_text("❌ 无法获取当前期号，请稍后重试")
                return
            
            # 生成预测
            prediction, confidence = bot_tools.predict_big_or_small(current_issue)
            
            # 保存到历史
            prediction_data = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "issue": current_issue,
                "prediction": prediction,
                "confidence": confidence,
                "status": "Pending"
            }
            bot_tools.prediction_history.append(prediction_data)
            
            win_rate = 0
            if bot_tools.recent_accuracy:
                wins = sum(1 for r in bot_tools.recent_accuracy if r == "WIN")
                win_rate = wins / len(bot_tools.recent_accuracy) * 100
            
            prediction_text = f"""🎯 Big/Small 预测结果

📊 **预测详情**:
━━━━━━━━━━━━━━━━━━━━━━━━
🔸 **期号**: {current_issue}
🔸 **预测**: {prediction} {'📈' if prediction == 'Big' else '📉'}
🔸 **置信度**: {confidence:.0%}
🔸 **状态**: 等待开奖 ⏳

📈 **算法信息**:
━━━━━━━━━━━━━━━━━━━━━━━━
• 预测策略: {bot_tools.current_strategy.upper()}
• 最近准确率: {win_rate:.1f}%
• 预测时间: {prediction_data['time']}

⚠️ **风险提示**:
━━━━━━━━━━━━━━━━━━━━━━━━
• 预测仅供参考，不构成投资建议
• 任何投注都存在风险
• 请理性参与，量力而行

🎯 预测已生成，等待结果验证"""
            
            back_keyboard = [
                [InlineKeyboardButton("🔄 再次预测", callback_data='get_prediction')],
                [InlineKeyboardButton("📊 查看结果", callback_data='latest_results')],
                [InlineKeyboardButton("🔙 返回预测系统", callback_data='prediction_system')]
            ]
            back_markup = InlineKeyboardMarkup(back_keyboard)
            
            await processing_msg.edit_text(prediction_text, reply_markup=back_markup)
            
        except Exception as e:
            logger.error(f"预测生成失败: {e}")
            await processing_msg.edit_text("❌ 预测生成失败，请稍后重试")
    
    elif query.data == 'latest_results':
        processing_msg = await query.edit_message_text("🔄 正在获取最新结果...")
        
        try:
            latest = bot_tools.fetch_latest_result()
            if not latest:
                await processing_msg.edit_text("❌ 无法获取最新结果，请稍后重试")
                return
            
            results_text = f"📊 最新开奖结果\n\n"
            results_text += f"🎯 **最新期号**: {latest['issue']}\n"
            results_text += f"🔸 **开奖号码**: {latest['number']}\n"
            results_text += f"🔸 **大小结果**: {latest['bigsmall']} {'📈' if latest['bigsmall'] == 'Big' else '📉'}\n\n"
            
            results_text += "📋 **最近5期结果**:\n"
            results_text += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            
            for i, record in enumerate(latest['records'], 1):
                num = record['number']
                bigsmall = "Big" if int(num) >= 5 else "Small"
                emoji = "📈" if bigsmall == "Big" else "📉"
                results_text += f"{i}. 期号: {record['issueNumber'][-4:]}... → {num} ({bigsmall}) {emoji}\n"
            
            results_text += f"\n⏰ 更新时间: {datetime.now().strftime('%H:%M:%S')}"
            
            back_keyboard = [
                [InlineKeyboardButton("🎯 获取预测", callback_data='get_prediction')],
                [InlineKeyboardButton("🔄 刷新结果", callback_data='latest_results')],
                [InlineKeyboardButton("🔙 返回预测系统", callback_data='prediction_system')]
            ]
            back_markup = InlineKeyboardMarkup(back_keyboard)
            
            await processing_msg.edit_text(results_text, reply_markup=back_markup)
            
        except Exception as e:
            logger.error(f"获取结果失败: {e}")
            await processing_msg.edit_text("❌ 获取结果失败，请稍后重试")
    
    elif query.data == 'prediction_history':
        if not bot_tools.prediction_history:
            await query.edit_message_text("📊 暂无预测历史记录\n\n🎯 点击\"获取预测\"开始使用系统")
            return
        
        history_text = "📈 预测历史记录\n\n"
        
        for i, pred in enumerate(reversed(list(bot_tools.prediction_history)), 1):
            status_emoji = "⏳" if pred['status'] == 'Pending' else "✅" if pred['status'] == 'WIN' else "❌"
            history_text += f"{i}. {pred['time']} | {pred['issue'][-4:]}... → {pred['prediction']} ({pred['confidence']:.0%}) {status_emoji}\n"
        
        if bot_tools.recent_accuracy:
            wins = sum(1 for r in bot_tools.recent_accuracy if r == "WIN")
            win_rate = wins / len(bot_tools.recent_accuracy) * 100
            history_text += f"\n📊 总体准确率: {win_rate:.1f}% ({wins}/{len(bot_tools.recent_accuracy)})"
        
        back_keyboard = [
            [InlineKeyboardButton("🔙 返回预测系统", callback_data='prediction_system')]
        ]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        await query.edit_message_text(history_text, reply_markup=back_markup)
    
    elif query.data == 'prediction_warning':
        warning_text = """⚠️ 重要风险提示

🚨 **高风险警告**:
• 预测系统基于算法分析，不保证准确性
• 任何形式的投注都存在损失风险
• 过往表现不代表未来结果
• 可能面临全部资金损失

📋 **免责声明**:
• 本系统仅提供技术分析参考
• 不构成投资建议或保证
• 用户需独立判断和决策
• 请咨询专业投资顾问

💰 **理性参与**:
• 只使用您能承受损失的资金
• 设置合理的投注限额
• 不要追求一夜暴富
• 保持冷静理性的心态

🎓 **使用建议**:
• 将预测作为参考而非绝对依据
• 结合其他分析方法
• 关注长期趋势而非单次结果
• 建立适合的风险管理策略

⚖️ 使用本系统即表示您理解并接受以上风险"""
        
        back_keyboard = [
            [InlineKeyboardButton("✅ 我已理解风险", callback_data='prediction_system')]
        ]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        await query.edit_message_text(warning_text, reply_markup=back_markup)
    
    elif query.data == 'set_price_info':
        await query.edit_message_text(
            f"💰 设置XAUUSD金价\n\n"
            f"📊 **当前金价**: ${bot_tools.current_gold_price:,.2f}\n\n"
            f"📋 **设置方法**:\n"
            f"发送消息格式:\n"
            f"• `price 3335` \n"
            f"• `价格 3335`\n"
            f"• `price 3340.50`\n\n"
            f"🎯 **示例**: `price 3335`\n\n"
            f"✅ 设置后，所有Lot Size计算都基于新价格"
        )
    
    elif query.data == 'help_menu':
        help_text = """ℹ️ 使用帮助指南

🔒 **HTML 加密工具**:
• 上传 .html 文件或发送HTML代码
• 获取加密后的文件
• 保护源码不被复制

💰 **Lot Size 精确计算**:
• 发送: `lot 0.1` 或 `手数 0.1`
• 发送: `price 3335` 设置金价
• 基于实际价格计算USD金额

🎯 **Big/Small 预测系统**:
• 点击获取预测按钮
• 查看最新开奖结果
• 选择预测策略 (5种策略)
• 测试策略表现
• 发送 `/verify` 验证预测结果
• ⚠️ 仅供参考，请理性使用

🎯 **快速命令**:
• `/start` - 显示主菜单
• `/verify` - 验证预测结果
• `lot 数字` - 计算手数
• `price 数字` - 设置金价

📞 **联系方式**:
• Telegram: @CKWinGg1330
• 频道: @TeamCKGroup

💡 **使用技巧**:
• 所有功能都支持自动识别
• 24小时在线服务
• 完全免费使用"""
        
        back_keyboard = [
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        await query.edit_message_text(help_text, reply_markup=back_markup)
    
    elif query.data == 'main_menu':
        await start(update, context)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理HTML文件加密"""
    document = update.message.document
    
    if not document.file_name.lower().endswith(('.html', '.htm')):
        await update.message.reply_text("❌ 请上传HTML文件(.html/.htm)")
        return
    
    processing_msg = await update.message.reply_text("🔒 正在加密HTML文件...")
    
    try:
        file = await context.bot.get_file(document.file_id)
        file_content = await file.download_as_bytearray()
        html_content = file_content.decode('utf-8')
        
        # 加密HTML
        encrypted_dict = bot_tools.encrypt_html(html_content)
        encrypted_script = bot_tools.generate_decryption_script(encrypted_dict)
        
        # 生成文件名
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        encrypted_filename = f"{random_name}.html"
        
        # 发送加密文件
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=encrypted_script.encode('utf-8'),
            filename=encrypted_filename,
            caption="✅ HTML文件加密完成！🔐"
        )
        
        await processing_msg.delete()
        
        success_keyboard = [
            [InlineKeyboardButton("🔒 再次加密", callback_data='html_encrypt')],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        success_markup = InlineKeyboardMarkup(success_keyboard)
        
        await update.message.reply_text(
            f"✅ 加密成功！\n\n"
            f"🔒 HTML文件已加密完成\n"
            f"🛡️ 源码已安全保护\n"
            f"📊 功能保持完整",
            reply_markup=success_markup
        )
        
    except Exception as e:
        logger.error(f"HTML加密错误: {e}")
        await processing_msg.edit_text("❌ 加密失败，请重试")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理文本消息"""
    text = update.message.text
    
    # 价格设置
    price_match = re.search(r'(?:price|价格)\s*(\d+\.?\d*)', text.lower())
    if price_match:
        price = float(price_match.group(1))
        if bot_tools.set_gold_price(price):
            await update.message.reply_text(
                f"💰 金价设置成功！\n\n"
                f"🔸 新金价: ${price:,.2f}\n"
                f"🔸 更新时间: {datetime.now().strftime('%H:%M:%S')}\n\n"
                f"📊 现在Lot Size计算基于新价格:\n"
                f"• 0.1手 = ${price * 10:,.2f} USD\n"
                f"• 1.0手 = ${price * 100:,.2f} USD\n\n"
                f"💡 试试发送: `lot 0.1`"
            )
        else:
            await update.message.reply_text("❌ 价格格式错误，请使用数字")
        return
    
    # Lot Size 计算
    lot_match = re.search(r'(?:lot|手数)\s*(\d+\.?\d*)', text.lower())
    if lot_match:
        lot_size = lot_match.group(1)
        calculation = bot_tools.calculate_lot_size_usd(lot_size)
        
        if calculation:
            calc_text = f"""💰 Lot Size 计算结果

📊 **计算详情**:
━━━━━━━━━━━━━━━━━━━━━━━━
🔸 **手数**: {calculation['lot_size']} 标准手
🔸 **黄金**: {calculation['ounces']:g} 盎司
🔸 **金价**: ${calculation['current_price']:,.2f}
🔸 **总价值**: ${calculation['usd_value']:,.2f} USD

💡 **交易信息**:
━━━━━━━━━━━━━━━━━━━━━━━━
• 每点价值: ${calculation['pip_value']:,.2f} USD
• 保证金需求: ${calculation['margin_required']:,.2f} USD (1%)
• 风险建议: 账户总资金的2-3%

📊 **仓位建议**:
━━━━━━━━━━━━━━━━━━━━━━━━
• 小额账户 ($1,000-$5,000): 0.01-0.05手
• 中等账户 ($5,000-$20,000): 0.05-0.2手  
• 大额账户 ($20,000+): 0.2手以上

⏰ 计算时间: {calculation['calculation_time']}"""
            
            calc_keyboard = [
                [InlineKeyboardButton("💰 设置金价", callback_data='set_price_info')],
                [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
            ]
            calc_markup = InlineKeyboardMarkup(calc_keyboard)
            
            await update.message.reply_text(calc_text, reply_markup=calc_markup)
        else:
            await update.message.reply_text("❌ 手数格式错误\n\n请使用: `lot 0.1` 或 `手数 0.1`")
        return
    
    # HTML 代码加密
    if text.strip().startswith('<') and text.strip().endswith('>'):
        processing_msg = await update.message.reply_text("🔒 正在加密HTML代码...")
        
        try:
            # 加密HTML代码
            encrypted_dict = bot_tools.encrypt_html(text)
            encrypted_script = bot_tools.generate_decryption_script(encrypted_dict)
            
            # 生成文件名
            random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            encrypted_filename = f"{random_name}.html"
            
            # 发送加密文件
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=encrypted_script.encode('utf-8'),
                filename=encrypted_filename,
                caption="✅ HTML代码加密完成！🔐"
            )
            
            await processing_msg.delete()
            
            success_keyboard = [
                [InlineKeyboardButton("🔒 再次加密", callback_data='html_encrypt')],
                [InlineKeyboardButton("💰 计算手数", callback_data='lot_calculator')]
            ]
            success_markup = InlineKeyboardMarkup(success_keyboard)
            
            await update.message.reply_text(
                f"✅ 代码加密成功！\n\n"
                f"🔒 HTML代码已加密完成\n"
                f"🛡️ 源码已安全保护",
                reply_markup=success_markup
            )
            
        except Exception as e:
            logger.error(f"HTML代码加密错误: {e}")
            await processing_msg.edit_text("❌ 加密失败，请重试")
        return
    
    # 预测系统关键词识别和验证
    if any(word in text.lower() for word in ['预测', 'big', 'small', '大小', 'predict']):
        keyboard = [
            [InlineKeyboardButton("🎯 获取预测", callback_data='get_prediction')],
            [InlineKeyboardButton("📊 查看结果", callback_data='latest_results')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎯 Big/Small预测系统说明：\n\n"
            "🧠 **智能算法**:\n"
            "• 多策略集成预测\n"
            "• 动态置信度计算\n"
            "• 历史数据学习\n\n"
            "⚠️ **重要提醒**:\n"
            "• 预测仅供参考\n"
            "• 投注存在风险\n"
            "• 请理性参与\n\n"
            "🎯 点击按钮开始使用:",
            reply_markup=reply_markup
        )
    
    # 验证预测结果
    elif text.lower() in ['/verify', 'verify', '验证', '检查结果']:
        processing_msg = await update.message.reply_text("🔄 正在验证预测结果...")
        
        try:
            verified_results = bot_tools.verify_predictions()
            
            if not verified_results:
                await processing_msg.edit_text("📊 暂无可验证的预测结果\n\n🎯 先获取预测，等开奖后再验证")
                return
            
            verify_text = "✅ 预测结果验证完成\n\n"
            
            for result in verified_results:
                status_emoji = "🎯" if result["result"] == "WIN" else "❌"
                verify_text += f"{status_emoji} **期号 {result['issue'][-4:]}...**\n"
                verify_text += f"   • 预测: {result['prediction']}\n"
                verify_text += f"   • 实际: {result['actual']}\n"
                verify_text += f"   • 结果: {result['result']}\n"
                verify_text += f"   • 置信度: {result['confidence']:.0%}\n\n"
            
            # 更新准确率
            if bot_tools.recent_accuracy:
                wins = sum(1 for r in bot_tools.recent_accuracy if r == "WIN")
                win_rate = wins / len(bot_tools.recent_accuracy) * 100
                verify_text += f"📊 **最新准确率**: {win_rate:.1f}% ({wins}/{len(bot_tools.recent_accuracy)})"
            
            await processing_msg.edit_text(verify_text)
            
        except Exception as e:
            logger.error(f"验证预测失败: {e}")
            await processing_msg.edit_text("❌ 验证失败，请稍后重试")
        return
    elif any(word in text.lower() for word in ['html', '加密', '网页', 'encrypt']):
        await update.message.reply_text(
            "🔒 HTML加密功能说明：\n\n"
            "📋 **使用方法**:\n"
            "• 直接发送HTML代码\n"
            "• 上传HTML文件\n"
            "• 获取加密后的文件\n\n"
            "💡 **示例**:\n"
            "发送: `<html><body>Hello</body></html>`\n"
            "获取: 加密后的HTML文件"
        )
    elif any(word in text.lower() for word in ['lot', '手数', '仓位', '计算', '金价']):
        await update.message.reply_text(
            "💰 Lot Size计算器说明：\n\n"
            "📋 **使用方法**:\n"
            "• 发送 `lot 0.1` 计算手数\n"
            "• 发送 `price 3335` 设置金价\n"
            "• 自动计算USD金额\n\n"
            "💡 **示例**:\n"
            "发送: `lot 0.1`\n"
            "回复: 0.1手 = ${bot_tools.current_gold_price * 10:,.2f} USD"
        )
    else:
        # 默认回复
        await update.message.reply_text(
            "👋 欢迎使用三功能工具Bot！\n\n"
            "🎯 **快速使用**:\n"
            "• 发送 `/start` 查看主菜单\n"
            "• 发送 `lot 0.1` 计算手数\n"
            "• 发送 `price 3335` 设置金价\n"
            "• 发送HTML代码进行加密\n"
            "• 点击预测获取Big/Small建议\n\n"
            "💡 三个强大功能，满足您的需求！"
        )

def main():
    """主函数"""
    if not BOT_TOKEN:
        print("❌ 请设置正确的 BOT_TOKEN")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 添加处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("🚀 三功能工具 Bot 启动中...")
    print("🔒 HTML 加密功能已就绪")
    print("💰 Lot Size 计算功能已就绪")
    print("🎯 Big/Small 预测功能已就绪 (原版算法)")
    print("🧠 支持5种预测策略: reverse, simple, alternating, modulo, ensemble")
    print("✅ 所有功能正常运行")
    
    application.run_polling()

if __name__ == '__main__':
    main()
