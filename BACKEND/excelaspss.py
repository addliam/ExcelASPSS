class ExcelASPSS:
    def __init__(self):
        # constantes
        self.CANTIDAD_RANGOS = 3
        pass
    
    def asignar_categoria_segun_rango(self, valor, diccionario_baremos):
        """
        Retorna la categoria (1,2,3) del valor segun los rangos del diccionario baremos
        """
        for key, rango in diccionario_baremos.items():
            if rango[0] <= valor <= rango[1]:
                return key
        return 0
    
    def baremos(self, puntuacion_maxima=5, cantidad_items=7, cantidad_rangos=3):
        """
        Retorna un diccionario conteniendo las categorias y baremos segun cantidad de items.
        """
        valor_minimo = cantidad_items
        valor_maximo = puntuacion_maxima * cantidad_items
        
        rango_total = valor_maximo - valor_minimo
        tamaño_grupo = rango_total // cantidad_rangos
        if rango_total % cantidad_rangos == 0:
            tamaño_grupo -= 1
                
        print(f"tamaño_grupo: {tamaño_grupo}")
        
        baremos_dict = {}
        inicio = valor_minimo
        
        for i in range(1, cantidad_rangos + 1):
            if i == cantidad_rangos:
                fin = valor_maximo
            else:
                fin = inicio + tamaño_grupo
            
            baremos_dict[i] = [inicio, fin]
            print(f"Categoria {i}: Rango: {inicio} - {fin} ==> Dif: {fin-inicio}")
            inicio = fin + 1
        
        print("")
        return baremos_dict
    
    def procesar(self, dataframe, items_total_variable1, items_total_variable2, explorar_dimensiones_de_v1, cantidad_item_por_dimensiones, numero_maximo_de_escala = 5):
        """
        Funcion central, recibe df y parametros de configuracion. 
        Retorna df procesado.
        NOTA: El df debe tener encabezado simple (P1,P2,P3,P4) y no contener datos sociodemograficos como edad, sexo.
        """
        df_copy = dataframe.copy()
        
        # Desde el indice 0 hasta la cantidad de items v1 agruparlos y sumar
        df_copy['TV1'] = df_copy.iloc[:, :items_total_variable1].sum(axis=1)
        df_copy['TV2'] = df_copy.iloc[:, items_total_variable1:items_total_variable1+items_total_variable2].sum(axis=1)
        baremos_variable1 = self.baremos(puntuacion_maxima=numero_maximo_de_escala,
                            cantidad_items=items_total_variable1,
                            cantidad_rangos=self.CANTIDAD_RANGOS)
        baremos_variable2 = self.baremos(puntuacion_maxima=numero_maximo_de_escala,
                            cantidad_items=items_total_variable2,
                            cantidad_rangos=self.CANTIDAD_RANGOS)
        
        # Categorias a variables 1 y 2
        df_copy['KTV1'] = df_copy['TV1'].apply(lambda x: self.asignar_categoria_segun_rango(x, baremos_variable1))
        df_copy['KTV2'] = df_copy['TV2'].apply(lambda x: self.asignar_categoria_segun_rango(x, baremos_variable2))
        
        # Asignar categorias a las dimensiones
        cursor_columna = 0
        if explorar_dimensiones_de_v1:
            for idx, cantidad_items_dimension in enumerate(cantidad_item_por_dimensiones):
                    # Crear columna acumulada F1, F2
                    df_copy[f'F{idx+1}'] = df_copy.iloc[:, cursor_columna:cursor_columna + cantidad_items_dimension].sum(axis=1)
                    
                    # Crear columna K{idx+1} para los baremos
                    baremos_dimension = self.baremos(puntuacion_maxima=numero_maximo_de_escala,
                                        cantidad_items=cantidad_items_dimension,
                                        cantidad_rangos=self.CANTIDAD_RANGOS)
                    df_copy[f'KF{idx+1}'] = df_copy[f'F{idx+1}'].apply(lambda x: self.asignar_categoria_segun_rango(x, baremos_dimension))
                    
                    # Actualiza la columna actual para la siguiente dimensión
                    cursor_columna += cantidad_items_dimension
                    
        # cuando pidan explorar dimensiones de v2 (caso menos comun)
        else:
            cursor_columna = items_total_variable1
            for idx, cantidad_items_dimension in enumerate(cantidad_item_por_dimensiones):
                # Crear columna acumulada F1, F2
                df_copy[f'F{idx+1}'] = df_copy.iloc[:, cursor_columna:cursor_columna + cantidad_items_dimension].sum(axis=1)
                
                # Crear columna K{idx+1} para los baremos
                baremos_dimension = self.baremos(puntuacion_maxima=numero_maximo_de_escala,
                                    cantidad_items=cantidad_items_dimension,
                                    cantidad_rangos=self.CANTIDAD_RANGOS)
                df_copy[f'KF{idx+1}'] = df_copy[f'F{idx+1}'].apply(lambda x: self.asignar_categoria_segun_rango(x, baremos_dimension))
                
                # Actualiza la columna actual para la siguiente dimensión
                cursor_columna += cantidad_items_dimension
        
        # Retornar dataframe procesado
        return df_copy