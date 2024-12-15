class Maze:
    def __init__(self, N):
        self.N = N
        # Инициализация лабиринта с непроходимыми стенами
        self.maze = [['█' for _ in range(N * 2 + 1)] for _ in range(N * 2 + 1)]
        for i in range(1, N * 2, 2):
            for j in range(1, N * 2, 2):
                self.maze[i][j] = '·'

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.maze)

    def __getitem__(self, key):
        x0, y0, x1, y1 = self._parse_key(key)
        return self._is_reachable(x0, y0, x1, y1)

    def __setitem__(self, key, value):
        x0, y0, x1, y1 = self._parse_key(key)
        if value == '·':
            self._open_passage(x0, y0, x1, y1)
        elif value == '█':
            self._close_passage(x0, y0, x1, y1)

    def _parse_key(self, key):
        # Парсинг ключа для получения координат
        x0, y0_x1, y1 = key
        y0, x1 = y0_x1.start, y0_x1.stop
        return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)

    def _is_reachable(self, x0, y0, x1, y1):
        # Проверка достижимости (поиск в ширину)
        if not (0 <= x0 < self.N and 0 <= y0 < self.N and 0 <= x1 < self.N and 0 <= y1 < self.N):
            return False

        from collections import deque

        queue = deque([(x0, y0)])
        visited = set()
        visited.add((x0, y0))

        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) == (x1, y1):
                return True

            # Проверяем все четыре направления
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.N and 0 <= ny < self.N and (nx, ny) not in visited:
                    if self.maze[2 * cy + 1 + dy][2 * cx + 1 + dx] == '·':
                        visited.add((nx, ny))
                        queue.append((nx, ny))

        return False

    def _open_passage(self, x0, y0, x1, y1):
        if x0 == x1:  # Вертикальное открытие
            for j in range(min(y0, y1), max(y0, y1)):
                self.maze[2 * j + 2][2 * x0 + 1] = '·'
        elif y0 == y1:  # Горизонтальное открытие
            for i in range(min(x0, x1), max(x0, x1)):
                self.maze[2 * y0 + 1][2 * i + 2] = '·'

    def _close_passage(self, x0, y0, x1, y1):
        if x0 == x1:  # Вертикальное открытие
            for j in range(min(y0, y1), max(y0, y1)):
                self.maze[2 * j + 2][2 * x0 + 1] = '█'
        elif y0 == y1:  # Горизонтальное открытие
            for i in range(min(x0, x1), max(x0, x1)):
                self.maze[2 * y0 + 1][2 * i + 2] = '█'

import sys
exec(sys.stdin.read())