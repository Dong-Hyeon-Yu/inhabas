package com.inhabas.api.domain.menu.repository;

import com.inhabas.api.domain.menu.domain.MenuGroup;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MenuGroupRepository extends JpaRepository<MenuGroup, Integer> {
}
