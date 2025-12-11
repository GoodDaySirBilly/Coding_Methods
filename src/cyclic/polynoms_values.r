n = 17          # Длина кода
k = 8           # Размерность кода
roots = [0, 1]  # Корни порождающего многочлена
field_degree = 8  # 1 для GF(2), >1 для GF(2^m)

print(f"Входные параметры:")
print(f"n = {n}, k = {k}")
print(f"Корни: {roots}")
print(f"Поле: GF(2^{field_degree})")
print("-" * 50)

if field_degree == 1:
    F = GF(2)
    print("Создано поле GF(2)")
    
    # Для GF(2) нужны корни в расширении поля
    # Найдем минимальное расширение, содержащее корни n-й степени из 1
    m_min = 1
    while True:
        if (2^m_min - 1) % n == 0:
            break
        m_min += 1
    
    print(f"   Для корней n-й степени из 1 требуется расширение GF(2^{m_min})")
    F_ext.<a> = GF(2^m_min, modulus='primitive')
    beta = a^((2^m_min - 1)/n)
    working_field = F_ext
    
else:
    # Случай GF(2^m), m > 1
    F.<a> = GF(2^field_degree, modulus='primitive')
    print(f"Создано поле GF(2^{field_degree})")
    print(f"   Примитивный элемент: a")
    print(f"   Порядок поля: {2^field_degree - 1}")
    working_field = F
    
    # Проверяем условие существования
    if (2^field_degree - 1) % n != 0:
        print(f"\nОШИБКА: n={n} не делит 2^{field_degree}-1 = {2^field_degree-1}")
        # Найдем минимальное подходящее m
        m_needed = field_degree
        while True:
            m_needed += 1
            if (2^m_needed - 1) % n == 0:
                break
        print(f"   Минимальное m, при котором n|(2^m-1): m={m_needed}")
        print("   Используйте это значение для field_degree")
    else:
        beta = a^((2^field_degree - 1)/n)

if 'beta' in locals():
    print(f"\n2. Найден элемент порядка {n}:")
    print(f"   beta = {beta}")
    print(f"   Проверка: beta^{n} = {beta^n}")
    
    print(f"\n3. Минимальные многочлены корней:")
    min_polys = []
    for r in roots:
        element = beta^r
        m_poly = element.minpoly()
        # Приводим коэффициенты к GF(2)
        coeffs = m_poly.coefficients(sparse=False)
        # Преобразуем коэффициенты из GF(2^m) в GF(2) через след
        binary_coeffs = []
        for coeff in coeffs:
            if coeff in GF(2):
                binary_coeffs.append(coeff)
            else:
                # Для элементов не из GF(2) берем коэффициент при x^0
                binary_coeffs.append(coeff.polynomial()[0])
        
        # Создаем полином с коэффициентами из GF(2)
        R_binary.<x> = PolynomialRing(GF(2))
        m_poly_binary = sum(binary_coeffs[i] * x^i for i in range(len(binary_coeffs)))
        
        min_polys.append(m_poly_binary)
        print(f"   Корень {r} (элемент beta^{r}):")
        print(f"   Минимальный многочлен в GF(2^{field_degree}): {m_poly}")
        print(f"   Приведенный к GF(2): m_{r}(x) = {m_poly_binary}")
    
    print(f"\n4. Порождающий многочлен g(x) в GF(2):")
    if len(min_polys) == 1:
        g = min_polys[0]
    else:
        g = min_polys[0]
        for poly in min_polys[1:]:
            g = lcm(g, poly)
    
    print(f"   g(x) = {g}")
    print(f"   Степень g(x): {g.degree()}")
    
    expected_degree = n - k
    actual_k = n - g.degree()
    
    if g.degree() != expected_degree:
        print(f"\n   ВНИМАНИЕ: степень g(x) = {g.degree()}, ожидалась {expected_degree}")
        print(f"   Фактический параметр: k = {actual_k}")
    else:
        print(f"\n   Совпадение: степень g(x) равна n-k = {expected_degree}")
        print(f"   k = {actual_k}")
    
    print(f"\n5. Проверочный многочлен h(x) в GF(2):")
    R_binary.<x> = PolynomialRing(GF(2))
    xn1_binary = x^n - 1
    h = xn1_binary // g
    print(f"   h(x) = {h}")
    print(f"   Степень h(x):{h.degree()}")
    
    print(f"\n6. Проверка: g(x)*h(x) = x^{n} - 1 в GF(2)")
    check_poly = g * h
    if check_poly == xn1_binary:
        print(f"   Верно! g(x)*h(x) = x^{n} - 1")
    else:
        print(f"   Ошибка! Произведение не равно x^{n} - 1")
        print(f"   Остаток: {xn1_binary - check_poly}")
    
    print(f"\n7. Параметры полученного кода:")
    print(f"   (n, k) = ({n}, {actual_k})")
    print(f"   Избыточность: r = {g.degree()}")
    
    if len(roots) > 0:
        d_min = max(roots) - min(roots) + 2
        print(f"   Оценка минимального расстояния (БЧХ): d ≥ {d_min}")
        print(f"   Код исправляет до t = {(d_min-1)//2} ошибок")
    
    print(f"\n8. Пример порождающей матрицы G (систематическая форма):")
    
    # Коэффициенты g(x) = g_0 + g_1*x + ... + g_r*x^r
    coeffs_g = g.coefficients(sparse=False)
    r = len(coeffs_g) - 1
    
    G_list = []
    for i in range(actual_k):
        # Сдвигаем g(x) на i позиций
        row = [0]*i + coeffs_g + [0]*(actual_k - i - 1)
        row = row[:n]  # Обрезаем до длины n
        G_list.append(row)
    
    G = matrix(GF(2), G_list)
    print(f"   Размер G: {G.dimensions()}")
    print(f"   G = ")
    print(G)
    
    print(f"\n9. Проверочная матрица H:")
    # Коэффициенты h(x) в обратном порядке
    coeffs_h = h.coefficients(sparse=False)
    H_list = []
    for i in range(r):
        row = [0]*i + list(reversed(coeffs_h)) + [0]*(r - i - 1)
        row = row[:n]
        H_list.append(row)
    
    H = matrix(GF(2), H_list)
    print(f"   Размер H: {H.dimensions()}")
    print(f"   H = ")
    print(H)
    
    # Проверка: G * H^T = 0
    print(f"\n10. Проверка: G * H^T = нулевая матрица")
    if G * H.transpose() == zero_matrix(GF(2), actual_k, r):
        print("   Проверка пройдена")
    else:
        print("   Ошибка!")

print("\n" + "="*50)