package hello.login.domain.video;

import lombok.Data;

@Data
public class Video {

    private Long id;

    private String date;


    public Video(String date) {
        this.date = date;
    }


}
