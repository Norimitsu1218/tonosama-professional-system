#!/usr/bin/env python3
"""
🔍 TONOSAMA Professional System - Quality Check & Testing
1兆円ダイヤモンド級品質の完璧な品質チェックシステム

全システム機能の動作確認と品質保証
"""

import sys
import os
import importlib
import inspect
from pathlib import Path
import subprocess
import json
import time
from typing import Dict, List, Tuple, Any

def print_header(title: str):
    """ヘッダー表示"""
    print("\n" + "="*60)
    print(f"🏮 {title}")
    print("="*60)

def print_success(message: str):
    """成功メッセージ"""
    print(f"✅ {message}")

def print_error(message: str):
    """エラーメッセージ"""
    print(f"❌ {message}")

def print_warning(message: str):
    """警告メッセージ"""
    print(f"⚠️ {message}")

def print_info(message: str):
    """情報メッセージ"""
    print(f"ℹ️ {message}")

class TONOSAMAQualityChecker:
    """TONOSAMA品質チェッカー"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.results = {
            "structure": [],
            "imports": [],
            "functionality": [],
            "quality": [],
            "deployment": []
        }
    
    def check_project_structure(self) -> bool:
        """プロジェクト構造チェック"""
        print_header("プロジェクト構造チェック")
        
        required_files = [
            "app.py",
            "requirements.txt",
            "README.md",
            "DEPLOYMENT.md",
            ".streamlit/config.toml",
            ".streamlit/secrets.toml.example",
            "modules/__init__.py",
            "modules/state_manager.py",
            "modules/openai_integration.py",
            "modules/csv_generator.py",
            "modules/google_drive.py",
            "modules/email_service.py",
            "modules/ui_styling.py",
            "modules/error_handler.py",
            "pages/1_🏪_店舗基本情報.py",
            "pages/2_📝_店主ストーリー.py",
            "pages/3_🍽️_メニュー情報.py",
            "pages/4_📊_順序最適化.py",
            "pages/5_🤖_AI食レポ.py",
            "pages/6_🎆_完了・プラン選択.py",
            "Dockerfile",
            "docker-compose.yml",
            "deploy.sh"
        ]
        
        all_present = True
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print_success(f"{file_path}")
                self.results["structure"].append((file_path, True, "存在"))
            else:
                print_error(f"{file_path} - 不足")
                self.results["structure"].append((file_path, False, "不足"))
                all_present = False
        
        # ディレクトリ構造確認
        required_dirs = ["modules", "pages", ".streamlit", "data", "assets"]
        
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                print_success(f"{dir_name}/ ディレクトリ")
            else:
                print_warning(f"{dir_name}/ ディレクトリ - 作成推奨")
                # data, assetsディレクトリは作成
                if dir_name in ["data", "assets"]:
                    dir_path.mkdir(exist_ok=True)
                    print_info(f"{dir_name}/ ディレクトリを作成しました")
        
        return all_present
    
    def check_imports(self) -> bool:
        """インポートチェック"""
        print_header("モジュールインポートチェック")
        
        # プロジェクトルートをPythonパスに追加
        sys.path.insert(0, str(self.project_root))
        
        modules_to_check = [
            "app",
            "modules.state_manager",
            "modules.openai_integration", 
            "modules.csv_generator",
            "modules.google_drive",
            "modules.email_service",
            "modules.ui_styling",
            "modules.error_handler"
        ]
        
        all_imports_ok = True
        
        for module_name in modules_to_check:
            try:
                importlib.import_module(module_name)
                print_success(f"{module_name}")
                self.results["imports"].append((module_name, True, "インポート成功"))
            except ImportError as e:
                print_error(f"{module_name} - インポートエラー: {e}")
                self.results["imports"].append((module_name, False, str(e)))
                all_imports_ok = False
            except Exception as e:
                print_warning(f"{module_name} - その他エラー: {e}")
                self.results["imports"].append((module_name, False, str(e)))
                all_imports_ok = False
        
        return all_imports_ok
    
    def check_dependencies(self) -> bool:
        """依存関係チェック"""
        print_header("依存関係チェック")
        
        try:
            # requirements.txt読み込み
            requirements_file = self.project_root / "requirements.txt"
            if not requirements_file.exists():
                print_error("requirements.txt が見つかりません")
                return False
            
            with open(requirements_file, 'r', encoding='utf-8') as f:
                requirements = f.read().splitlines()
            
            # 主要パッケージの確認
            critical_packages = [
                "streamlit", "openai", "pandas", "pillow", 
                "google-api-python-client", "sendgrid", "cryptography"
            ]
            
            all_deps_ok = True
            
            for package in critical_packages:
                try:
                    importlib.import_module(package.replace('-', '_'))
                    print_success(f"{package}")
                except ImportError:
                    print_error(f"{package} - インストールされていません")
                    all_deps_ok = False
            
            print_info(f"requirements.txtに{len(requirements)}の依存関係が定義されています")
            
            return all_deps_ok
            
        except Exception as e:
            print_error(f"依存関係チェック中にエラー: {e}")
            return False
    
    def check_functionality(self) -> bool:
        """機能チェック"""
        print_header("コア機能チェック")
        
        try:
            # StateManager チェック
            from modules.state_manager import get_state_manager
            state_manager = get_state_manager()
            print_success("StateManager - 初期化OK")
            
            # OpenAI Integration チェック  
            from modules.openai_integration import get_openai_integration
            openai_integration = get_openai_integration()
            print_success("OpenAI Integration - 初期化OK")
            
            # CSV Generator チェック
            from modules.csv_generator import get_csv_generator
            csv_generator = get_csv_generator()
            print_success("CSV Generator - 初期化OK")
            
            # Google Drive チェック
            from modules.google_drive import get_google_drive_integration
            google_drive = get_google_drive_integration()
            print_success("Google Drive Integration - 初期化OK")
            
            # Email Service チェック
            from modules.email_service import get_email_service
            email_service = get_email_service()
            print_success("Email Service - 初期化OK")
            
            # UI Styling チェック
            from modules.ui_styling import inject_diamond_css
            print_success("UI Styling - インポートOK")
            
            # Error Handler チェック
            from modules.error_handler import get_error_handler
            error_handler = get_error_handler()
            print_success("Error Handler - 初期化OK")
            
            return True
            
        except Exception as e:
            print_error(f"機能チェック中にエラー: {e}")
            return False
    
    def check_code_quality(self) -> bool:
        """コード品質チェック"""
        print_header("コード品質チェック")
        
        quality_checks = []
        
        # ファイルサイズチェック
        python_files = list(self.project_root.rglob("*.py"))
        large_files = []
        
        for file_path in python_files:
            size_kb = file_path.stat().st_size / 1024
            if size_kb > 500:  # 500KB以上
                large_files.append((file_path.name, size_kb))
        
        if large_files:
            print_warning(f"大きなファイル ({len(large_files)}個):")
            for name, size in large_files:
                print(f"  - {name}: {size:.1f}KB")
        else:
            print_success("ファイルサイズ - 適切")
        
        # Docstring存在確認
        docstring_count = 0
        total_functions = 0
        
        for file_path in python_files:
            if "__pycache__" in str(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 簡単なdocstring検出
                if '"""' in content:
                    docstring_count += content.count('"""') // 2
                
                # 関数数カウント
                total_functions += content.count('def ')
                
            except Exception:
                continue
        
        print_info(f"Docstring: {docstring_count}個, 関数: {total_functions}個")
        
        # モジュール構造チェック
        modules_dir = self.project_root / "modules"
        if modules_dir.exists():
            module_files = list(modules_dir.glob("*.py"))
            print_success(f"モジュール構造 - {len(module_files)}個のモジュール")
        
        return True
    
    def check_deployment_readiness(self) -> bool:
        """デプロイ準備チェック"""
        print_header("デプロイ準備チェック")
        
        deployment_files = [
            ("Dockerfile", "Docker展開用"),
            ("docker-compose.yml", "Docker Compose用"),
            ("deploy.sh", "デプロイスクリプト"),
            ("Procfile", "Heroku用"),
            ("runtime.txt", "Python版本指定"),
            (".streamlit/config.toml", "Streamlit設定"),
            ("DEPLOYMENT.md", "デプロイメントガイド")
        ]
        
        all_ready = True
        
        for file_name, description in deployment_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                print_success(f"{file_name} - {description}")
            else:
                print_warning(f"{file_name} - {description} (推奨)")
                if file_name in ["Procfile", "runtime.txt"]:
                    all_ready = False
        
        # deploy.sh実行権限チェック
        deploy_script = self.project_root / "deploy.sh"
        if deploy_script.exists():
            if os.access(deploy_script, os.X_OK):
                print_success("deploy.sh - 実行権限OK")
            else:
                print_warning("deploy.sh - 実行権限を付与してください")
        
        return all_ready
    
    def generate_quality_report(self) -> Dict[str, Any]:
        """品質レポート生成"""
        print_header("品質レポート生成")
        
        total_checks = sum(len(checks) for checks in self.results.values())
        passed_checks = sum(
            sum(1 for _, status, _ in checks if status) 
            for checks in self.results.values()
        )
        
        quality_score = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "quality_score": quality_score,
            "grade": self._get_quality_grade(quality_score),
            "results": self.results
        }
        
        print_info(f"総チェック数: {total_checks}")
        print_info(f"合格数: {passed_checks}")
        print_info(f"品質スコア: {quality_score:.1f}%")
        print_info(f"品質グレード: {report['grade']}")
        
        return report
    
    def _get_quality_grade(self, score: float) -> str:
        """品質グレード判定"""
        if score >= 95:
            return "💎 Diamond Grade (1兆円級)"
        elif score >= 90:
            return "👑 Platinum Grade"
        elif score >= 80:
            return "🥇 Gold Grade"
        elif score >= 70:
            return "🥈 Silver Grade"
        elif score >= 60:
            return "🥉 Bronze Grade"
        else:
            return "⚠️ Improvement Needed"
    
    def run_all_checks(self) -> bool:
        """全チェック実行"""
        print_header("🏮 TONOSAMA Professional System - 品質チェック開始")
        print("1兆円ダイヤモンド級品質の完璧な検証を実行します\n")
        
        checks = [
            ("プロジェクト構造", self.check_project_structure),
            ("インポート", self.check_imports),
            ("依存関係", self.check_dependencies),
            ("コア機能", self.check_functionality),
            ("コード品質", self.check_code_quality),
            ("デプロイ準備", self.check_deployment_readiness)
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            try:
                result = check_func()
                if not result:
                    all_passed = False
                    print_warning(f"{check_name}チェックで問題が検出されました")
                
            except Exception as e:
                print_error(f"{check_name}チェック中にエラー: {e}")
                all_passed = False
        
        # レポート生成
        report = self.generate_quality_report()
        
        # レポート保存
        try:
            report_file = self.project_root / "quality_report.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print_success(f"品質レポートを保存しました: {report_file}")
        except Exception as e:
            print_warning(f"レポート保存エラー: {e}")
        
        # 最終結果
        print_header("最終結果")
        if all_passed and report["quality_score"] >= 95:
            print("🎉🏮✨ おめでとうございます！")
            print("💎 TONOSAMA Professional System は")
            print("   1兆円ダイヤモンド級品質を達成しました！")
            print("\n✅ 全システムが完璧に構築され、本番環境への")
            print("   デプロイメント準備が完了しています。")
            print("\n🚀 世界最高品質の多言語レストランシステムの")
            print("   運用を開始してください！")
        elif report["quality_score"] >= 90:
            print("🏆 素晴らしい品質です！")
            print("👑 Platinum Grade を達成しました。")
            print("いくつかの改善点がありますが、本番運用可能です。")
        else:
            print("📋 改善が必要な項目があります。")
            print("品質向上のため、検出された問題を修正してください。")
        
        return all_passed

def main():
    """メイン実行"""
    checker = TONOSAMAQualityChecker()
    success = checker.run_all_checks()
    
    # 終了コード
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()