SELECT C_Comps.c_name AS country_name, 
		 COUNT(DISTINCT C_Comps.id) AS companies_count FROM
	(SELECT Countries.id as count_id,
		Countries.name as c_name,
		 Comps.id,
		 Comps.labors FROM
		(SELECT Companies.id,
		 Companies.labors,
		 Cities.country_id
		FROM Companies
		LEFT JOIN Cities
			ON Companies.city_id = Cities.id) AS Comps
		RIGHT JOIN Countries
			ON Countries.id = Comps.country_id) AS C_Comps
	WHERE (C_Comps.labors >= 1000)
	GROUP BY (C_Comps.c_name);