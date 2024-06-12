from seachad.calcs.calc import sum
import seachad.common_libraries.terminal_colors as tc
import seachad.common_libraries.cache_REDIS as cr

if __name__ == '__main__':
    print("resultado de la operación sum")
    print(sum(1, 2))
    print("ahora a por terminal colors")
    tc.test_print()
    
    cr.test_cache()