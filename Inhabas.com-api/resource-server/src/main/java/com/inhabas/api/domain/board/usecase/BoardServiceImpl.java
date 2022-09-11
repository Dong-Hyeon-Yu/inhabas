package com.inhabas.api.domain.board.usecase;

import com.inhabas.api.domain.board.BoardCannotModifiableException;
import com.inhabas.api.domain.board.BoardNotFoundException;
import com.inhabas.api.domain.board.domain.NormalBoard;
import com.inhabas.api.domain.board.repository.NormalBoardRepository;
import com.inhabas.api.domain.member.domain.valueObject.MemberId;
import com.inhabas.api.domain.menu.domain.valueObject.MenuId;
import com.inhabas.api.domain.board.dto.BoardDto;
import com.inhabas.api.domain.board.dto.SaveBoardDto;
import com.inhabas.api.domain.board.dto.UpdateBoardDto;
import javax.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@Transactional
@RequiredArgsConstructor
public class BoardServiceImpl implements BoardService {

    private final NormalBoardRepository boardRepository;

    @Override
    public Integer write(MemberId memberId, SaveBoardDto saveBoardDto) {

        NormalBoard normalBoard = new NormalBoard(saveBoardDto.getTitle(), saveBoardDto.getContents())
                .inMenu(saveBoardDto.getMenuId())
                .writtenBy(memberId);

        return boardRepository.save(normalBoard).getId();
    }

    @Override
    public Integer update(MemberId memberId, UpdateBoardDto updateBoardDto) {

        NormalBoard savedBoard = boardRepository.findById(updateBoardDto.getId())
                .orElseThrow(BoardNotFoundException::new);

        savedBoard.modify(updateBoardDto.getTitle(), updateBoardDto.getContents(), memberId);

        return boardRepository.save(savedBoard).getId();
    }

    @Override
    public void delete(MemberId memberId, Integer boardId) {

        NormalBoard board = boardRepository.findById(boardId)
                .orElseThrow(BoardNotFoundException::new);

        if (board.cannotModifiableBy(memberId)) {
            throw new BoardCannotModifiableException();
        }

        boardRepository.deleteById(boardId);
    }

    @Override
    public BoardDto getBoard(Integer id) {

        return boardRepository.findDtoById(id)
                .orElseThrow(BoardNotFoundException::new);
    }

    @Override
    public Page<BoardDto> getBoardList(MenuId menuId, Pageable pageable) {

            return boardRepository.findAllByMenuId(menuId, pageable);
    }
}
