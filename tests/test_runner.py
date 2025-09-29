"""
テストランナー
"""
import unittest
import sys
import os
import time

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_specific_test(test_module):
    """特定のテストモジュールを実行"""
    try:
        # テストモジュールをインポート
        module = __import__(f'tests.{test_module}', fromlist=[''])
        
        # テストスイートを作成
        suite = unittest.TestLoader().loadTestsFromModule(module)
        
        # テストランナーを作成
        runner = unittest.TextTestRunner(verbosity=2)
        
        # テストを実行
        result = runner.run(suite)
        
        return result
        
    except ImportError as e:
        print(f"Error importing test module {test_module}: {e}")
        return None
    except Exception as e:
        print(f"Error running test module {test_module}: {e}")
        return None

def run_all_tests():
    """すべてのテストを実行"""
    test_modules = [
        'test_content_analyzer',
        'test_config',
        'test_data_transformer',
        'test_conflict_resolver',
        'test_event_manager',
        'test_markdown_parser',
        'test_insight_generator',
        'test_recommendation_system',
        'test_analysis_engine',
        'test_sync_coordinator',
        'test_notion_client',
        'test_obsidian_file_monitor',
        'test_main'
    ]
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    
    print("=" * 80)
    print("Running All Tests")
    print("=" * 80)
    
    start_time = time.time()
    
    for test_module in test_modules:
        print(f"\nRunning {test_module}...")
        print("-" * 40)
        
        result = run_specific_test(test_module)
        
        if result:
            total_tests += result.testsRun
            total_failures += len(result.failures)
            total_errors += len(result.errors)
            total_skipped += len(result.skipped)
            
            print(f"Tests run: {result.testsRun}")
            print(f"Failures: {len(result.failures)}")
            print(f"Errors: {len(result.errors)}")
            print(f"Skipped: {len(result.skipped)}")
            
            if result.failures:
                print("\nFailures:")
                for test, traceback in result.failures:
                    print(f"  {test}: {traceback}")
            
            if result.errors:
                print("\nErrors:")
                for test, traceback in result.errors:
                    print(f"  {test}: {traceback}")
        else:
            print(f"Failed to run {test_module}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    print(f"Total tests run: {total_tests}")
    print(f"Total failures: {total_failures}")
    print(f"Total errors: {total_errors}")
    print(f"Total skipped: {total_skipped}")
    print(f"Duration: {duration:.2f} seconds")
    
    if total_failures == 0 and total_errors == 0:
        print("\n✅ All tests passed!")
        return True
    else:
        print(f"\n❌ {total_failures + total_errors} test(s) failed")
        return False

def run_quick_tests():
    """クイックテストを実行（基本的なテストのみ）"""
    quick_test_modules = [
        'test_config',
        'test_data_transformer',
        'test_conflict_resolver',
        'test_event_manager',
        'test_markdown_parser'
    ]
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    print("=" * 80)
    print("Running Quick Tests")
    print("=" * 80)
    
    start_time = time.time()
    
    for test_module in quick_test_modules:
        print(f"\nRunning {test_module}...")
        print("-" * 40)
        
        result = run_specific_test(test_module)
        
        if result:
            total_tests += result.testsRun
            total_failures += len(result.failures)
            total_errors += len(result.errors)
            
            print(f"Tests run: {result.testsRun}")
            print(f"Failures: {len(result.failures)}")
            print(f"Errors: {len(result.errors)}")
        else:
            print(f"Failed to run {test_module}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 80)
    print("Quick Test Summary")
    print("=" * 80)
    print(f"Total tests run: {total_tests}")
    print(f"Total failures: {total_failures}")
    print(f"Total errors: {total_errors}")
    print(f"Duration: {duration:.2f} seconds")
    
    if total_failures == 0 and total_errors == 0:
        print("\n✅ All quick tests passed!")
        return True
    else:
        print(f"\n❌ {total_failures + total_errors} test(s) failed")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'quick':
            success = run_quick_tests()
        elif sys.argv[1] == 'all':
            success = run_all_tests()
        else:
            print("Usage: python test_runner.py [quick|all]")
            sys.exit(1)
    else:
        print("Usage: python test_runner.py [quick|all]")
        print("  quick: Run quick tests (basic functionality)")
        print("  all:   Run all tests")
        sys.exit(1)
    
    sys.exit(0 if success else 1)
